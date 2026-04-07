"""
🚀 Weekly Tech Digest Scraper - Core Data Extraction Module
This module handles fetching data from Hacker News and DEV.to, 
calculating engagement, and deduplicating cross-platform articles.
"""

import requests
import time
import logging
from fuzzywuzzy import fuzz

# Configure basic logging for internal monitoring
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def fetch_hackernews(limit: int = 20) -> list[dict]:
    """
    📥 Fetches top stories from Hacker News using the Firebase API.
    
    The process involves:
    1. Grabbing a list of top story IDs.
    2. Fetching individual details for each ID.
    
    Args:
        limit (int): Number of top stories to inspect. Defaults to 20.
    Returns:
        list[dict]: Normalized article data.
    """
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3) # Add retries for stability
    session.mount('https://', adapter)
    
    try:
        # Step 1: Get the current top 500 story IDs
        response = session.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=10)
        response.raise_for_status()
        story_ids = response.json()
    except Exception as e:
        logging.error(f"❌ Failed to reach HN API: {e}")
        return []

    articles = []
    # Step 2: Fetch details for the first 'limit' stories
    for story_id in story_ids[:limit]:
        try:
            item_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            item_response = session.get(item_url, timeout=10)
            item_response.raise_for_status()
            item = item_response.json()

            # Filter: We only want 'stories' that have external URLs
            if not item or item.get('type') != 'story' or 'url' not in item:
                continue

            # Standardize the data structure
            articles.append({
                'title': item.get('title'),
                'url': item.get('url'),
                'votes': item.get('score', 0),
                'comments': item.get('descendants', 0),
                'tags': [],  # HN doesn't provide tags natively
                'platform': 'Hacker News'
            })
            
            # Rate limiting: Be polite to the API (50ms gap)
            time.sleep(0.05)
            
        except Exception as e:
            # If one story fails, log it but don't crash the entire list
            logging.warning(f"⚠️ Skipping HN item {story_id} due to error: {e}")
            continue

    return articles

def fetch_devto(limit: int = 20) -> list[dict]:
    """
    📥 Fetches top articles from DEV.to in a single batch call.
    
    Args:
        limit (int): Number of top articles to fetch. Defaults to 20.
    Returns:
        list[dict]: Normalized article data.
    """
    # DEV.to API allows fetching top articles directly with pagination/limit
    url = f'https://dev.to/api/articles?top=1&per_page={limit}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        # If the API call fails, we let the caller know so they can decide how to handle it
        raise Exception(f"❌ DEV.to API request failed: {e}")

    # Transform DEV.to specific fields into our internal format
    articles = []
    for item in data:
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
    ⚖️ Calculates the priority score based on user interaction.
    
    Formula: (Votes * 1.0) + (Comments * 1.5)
    Note: Comments are weighted higher (1.5x) as they represent deeper engagement.
    
    Args:
        article (dict): The article to score.
    Returns:
        float: The final engagement score.
    """
    votes = article.get('votes', 0)
    comments = article.get('comments', 0)
    score = (votes * 1.0) + (comments * 1.5)
    
    # Store the score directly on the object for easier sorting later
    article['engagement_score'] = score
    return score

def deduplicate(articles: list[dict], threshold: int = 80) -> list[dict]:
    """
    🧹 Removes duplicate articles across different platforms using fuzzy title matching.
    
    Args:
        articles (list[dict]): The raw combined list of articles.
        threshold (int): Similarity score (0-100) to trigger a duplicate detection.
    Returns:
        list[dict]: A clean list with the 'better' (higher engagement) version of each story.
    """
    kept_articles = []
    
    for article in articles:
        is_duplicate = False
        # Compare current article against everything we've already decided to keep
        for kept in kept_articles:
            # We use token_sort_ratio to ignore word order differences
            similarity = fuzz.token_sort_ratio(article['title'], kept['title'])
            
            if similarity > threshold:
                is_duplicate = True
                # Conflict resolution: Keep the version with higher engagement
                if article['engagement_score'] > kept['engagement_score']:
                    kept_articles.remove(kept)
                    kept_articles.append(article)
                break
        
        # If it's a unique story, add it to our collection
        if not is_duplicate:
            kept_articles.append(article)
            
    return kept_articles

def get_top_articles(top_n: int = 10) -> tuple[list[dict], int]:
    """
    ⚙️ The main coordination function for data collection.
    
    Returns:
        tuple[list[dict], int]: (Top N articles, Total fetched count)
    """
    # 1. Fetch from multiple sources with individual error handling
    try:
        hn_articles = fetch_hackernews()
    except Exception as e:
        logging.error(f"⚠️ HN integration stalled: {e}")
        hn_articles = []

    try:
        dev_articles = fetch_devto()
    except Exception as e:
        logging.error(f"⚠️ DEV.to integration stalled: {e}")
        dev_articles = []
    
    # 2. Critical Check: Fail if there is no data at all
    if not hn_articles and not dev_articles:
        raise RuntimeError("🚫 All sources returned no data. Aborting pipeline.")
    
    combined = hn_articles + dev_articles
    total_fetched = len(combined)
    
    # 3. Process: Score and Deduplicate
    for article in combined:
        calculate_engagement(article)
    
    deduplicated = deduplicate(combined)
    
    # 4. Final Ranking: Sort by score (descending)
    deduplicated.sort(key=lambda x: x['engagement_score'], reverse=True)
    
    # 5. Output the result set
    return deduplicated[:top_n], total_fetched
