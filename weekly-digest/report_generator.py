import os
from datetime import datetime
import jinja2
from scraper import get_top_articles

def generate_report(articles: list[dict], output_path: str = "output/weekly_digest.html", total_before_dedup: int = 0) -> str:
    """
    Generate an HTML report using Jinja2 and save it to the specified output path.

    Args:
        articles (list[dict]): List of deduplicated top articles.
        output_path (str): Path where the HTML report will be saved.
        total_before_dedup (int): Total number of articles considered before deduplication.

    Returns:
        str: The path to the generated HTML report.
    """
    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load the Jinja2 template from templates/digest.html
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
    try:
        template = env.get_template("digest.html")
    except jinja2.TemplateNotFound:
        # Fallback if acting within the weekly-digest directory
        env = jinja2.Environment(loader=jinja2.FileSystemLoader("weekly-digest/templates"))
        template = env.get_template("digest.html")

    # Pass to the template: articles, generated_at, total_considered
    generated_at = datetime.now().strftime("%A, %d %B %Y at %H:%M")
    
    html_content = template.render(
        articles=articles,
        generated_at=generated_at,
        total_considered=total_before_dedup
    )

    # Write the rendered HTML to output_path
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Report saved to {output_path}")
    return output_path

if __name__ == "__main__":
    # Test the full pipeline
    print("Testing pipeline...")
    # Update to handle the tuple (articles, total_fetched)
    top_articles, total_fetched = get_top_articles(top_n=10)
    
    generate_report(top_articles, total_before_dedup=total_fetched)
