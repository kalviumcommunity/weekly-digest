import requests
import time
from fuzzywuzzy import fuzz

def fetch_hackernews(limit=20) -> list[dict]:
    """
    Fetch the top story IDs from the Hacker News Firebase API.

    Args:
        limit (int): Number of stories to fetch. Defaults to 20.

    Returns:
        list[dict]: A list of dictionary objects representing Hacker News stories.
    """
    session = requests.Session()
    # Fetch the top story IDs from the Firebase API
    try:
        response = session.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=10)
        response.raise_for_status()
        story_ids = response.json()
    except Exception as e:
        print(f"Error fetching Hacker News top stories: {e}")
        return []

    articles = []
    # For each of the first limit IDs, fetch the item JSON
    for story_id in story_ids[:limit]:
        try:
            item_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            item_response = session.get(item_url, timeout=10)
            item_response.raise_for_status()
            item = item_response.json()

            # Skip items where type is not story or where url is missing
            if not item or item.get('type') != 'story' or 'url' not in item:
                continue

            # Return a list of dicts with specified keys
            articles.append({
                'title': item.get('title'),
                'url': item.get('url'),
                'votes': item.get('score', 0),
                'comments': item.get('descendants', 0),
                'tags': [],  # HN has no tags
                'platform': 'Hacker News'
            })
            # Add a time.sleep(0.05) between item fetches to be a polite API consumer
            time.sleep(0.05)
        except Exception as e:
            # Wrap each item fetch in a try/except and skip failed items with a printed warning
            print(f"Warning: Failed to fetch HN item {story_id}: {e}")
            continue

    return articles

def fetch_devto(limit=20) -> list[dict]:
    """
    Fetch the top articles from the DEV.to API.

    Args:
        limit (int): Number of articles to fetch. Defaults to 20.

    Returns:
        list[dict]: A list of dictionary objects representing DEV.to articles.
    """
    url = f'https://dev.to/api/articles?top=1&per_page={limit}'
    try:
        # Make a single GET to DEV.to top articles endpoint
        response = requests.get(url, timeout=10)
        # Handle non-200 responses by raising a descriptive exception
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise Exception(f"Error fetching DEV.to articles: {e}")

    articles = []
    for item in data:
        # Return a list of dicts with the same keys
        articles.append({
            'title': item.get('title'),
            'url': item.get('canonical_url'),
            'votes': item.get('positive_reactions_count', 0),
            'comments': item.get('comments_count', 0),
            'tags': item.get('tag_list', []),
            'platform': 'DEV.to'
        })
    return articles

def calculate_engagement(article: dict) -> float:
    """
    Calculate an engagement score based on votes and comments.

    Args:
        article (dict): The article dictionary object.

    Returns:
        float: The calculated engagement score.
    """
    # Apply the formula: score = (votes * 1.0) + (comments * 1.5)
    votes = article.get('votes', 0)
    comments = article.get('comments', 0)
    score = (votes * 1.0) + (comments * 1.5)
    
    # Add this score as an engagement_score key directly on the article dict
    article['engagement_score'] = score
    return score

def deduplicate(articles: list[dict], threshold: int = 80) -> list[dict]:
    """
    Deduplicate a list of articles based on title similarity.

    Args:
        articles (list[dict]): The list of articles to deduplicate.
        threshold (int): Similarity threshold for deduplication. Defaults to 80.

    Returns:
        list[dict]: A deduplicated list of articles.
    """
    kept_articles = []
    
    # Use a greedy approach: iterate in order
    for article in articles:
        is_duplicate = False
        # For each article, compare its title against all previously seen titles
        for kept in kept_articles:
            similarity = fuzz.token_sort_ratio(article['title'], kept['title'])
            # If similarity is above threshold, treat as duplicates
            if similarity > threshold:
                is_duplicate = True
                # Keep only the one with the higher engagement_score
                if article['engagement_score'] > kept['engagement_score']:
                    # Replace the existing article in the kept list
                    kept_articles.remove(kept)
                    kept_articles.append(article)
                break
        
        # If not a duplicate or it replaced a duplicate, it was already handled
        if not is_duplicate:
            kept_articles.append(article)
            
    return kept_articles

def get_top_articles(top_n: int = 10) -> tuple[list[dict], int]:
    """
    Combine Hacker News and DEV.to articles, deduplicate and return top results.

    Args:
        top_n (int): Number of top articles to return. Defaults to 10.

    Returns:
        tuple[list[dict], int]: A tuple containing the sorted and deduplicated list of top articles 
                               and the total number of articles fetched before deduplication.
    """
    # Call fetch_hackernews() and fetch_devto()
    try:
        hn_articles = fetch_hackernews()
    except Exception as e:
        print(f"Warning: Hacker News API is temporarily down: {e}")
        hn_articles = []

    try:
        dev_articles = fetch_devto()
    except Exception as e:
        print(f"Warning: DEV.to API is temporarily down: {e}")
        dev_articles = []
    
    # If both return empty, raise a RuntimeError
    if not hn_articles and not dev_articles:
        raise RuntimeError("Both sources returned no data. Aborting report generation.")
    
    combined = hn_articles + dev_articles
    total_fetched = len(combined)
    
    # Call calculate_engagement() on every article in the combined list
    for article in combined:
        calculate_engagement(article)
    
    # Call deduplicate() on the combined list
    deduplicated = deduplicate(combined)
    
    # Sort by engagement_score descending
    deduplicated.sort(key=lambda x: x['engagement_score'], reverse=True)
    
    # Return the top top_n articles and the total count
    return deduplicated[:top_n], total_fetched
