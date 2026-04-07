"""
🎨 Weekly Tech Digest - Report Generator
This module transforms raw article data into a premium HTML experience
using Jinja2 templates.
"""

import os
from datetime import datetime
import jinja2
from scraper import get_top_articles

def generate_report(articles: list[dict], output_path: str = "output/weekly_digest.html", total_before_dedup: int = 0) -> str:
    """
    🏗️ Builds the final HTML report and saves it to disk.

    Args:
        articles (list[dict]): The curated list of top stories.
        output_path (str): File destination.
        total_before_dedup (int): Stats for the footer.

    Returns:
        str: Absolute path to the generated file.
    """
    # 📁 Ensure the output directory exists (avoid FileNotFoundError)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 🧩 Initialize Jinja2 Environment
    # We check multiple possible locations for the template to ensure portability
    template_dirs = ["templates", "weekly-digest/templates", "../templates"]
    loader = jinja2.FileSystemLoader(template_dirs)
    env = jinja2.Environment(loader=loader)
    
    try:
        template = env.get_template("digest.html")
    except jinja2.TemplateNotFound:
        # Emergency fallback for different execution contexts
        raise FileNotFoundError("❌ Could not find 'digest.html' in expected template directories.")

    # ⏰ Prepare Meta Data
    generated_at = datetime.now().strftime("%A, %d %B %Y at %H:%M")
    
    # 🖌️ Render the HTML
    html_content = template.render(
        articles=articles,
        generated_at=generated_at,
        total_considered=total_before_dedup
    )

    # 💾 Persist to Disk
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Success! Report generated at: {output_path}")
    return output_path

if __name__ == "__main__":
    # 🛠️ Manual Testing Entry Point
    print("🚀 Triggering manual report generation...")
    
    try:
        # Fetch data using our scraper coordination function
        top_articles, total_fetched = get_top_articles(top_n=10)
        
        # Build the report
        generate_report(top_articles, total_before_dedup=total_fetched)
        
    except Exception as e:
        print(f"💥 Pipeline failed during manual run: {e}")
