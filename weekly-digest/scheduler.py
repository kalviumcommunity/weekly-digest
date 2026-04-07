# cron alternative (add to crontab with: crontab -e)
# 0 9 * * 1 /usr/bin/python3 /path/to/project/scheduler.py

import os
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from scraper import get_top_articles
from report_generator import generate_report

# Configure logging
os.makedirs("output", exist_ok=True)
logging.basicConfig(
    filename='output/error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_weekly_digest():
    """
    Main pipeline task: fetch articles, generate report, and handle errors.
    """
    try:
        print(f"[{datetime.now()}] Starting weekly digest run...")
        
        # Call get_top_articles(top_n=10) inside a try/except
        articles, total_fetched = get_top_articles(top_n=10)
        
        # Call generate_report() with the total_before_dedup count
        output_path = generate_report(articles, total_before_dedup=total_fetched)
        
        # Print a completion message with the timestamp and number of articles
        print(f"[{datetime.now()}] Success: Report generated with {len(articles)} articles.")
        print(f"Location: {output_path}")
        
    except Exception as e:
        # Logs the error to a file output/error.log with a timestamp and re-raises
        logging.error(f"Pipeline failed: {str(e)}")
        print(f"[{datetime.now()}] ERROR: {str(e)}. Check output/error.log for details.")
        raise e

if __name__ == "__main__":
    # Set up an APScheduler BlockingScheduler
    scheduler = BlockingScheduler()
    
    # Trigger run_weekly_digest using a CronTrigger: Monday at 9:00 AM
    trigger = CronTrigger(day_of_week='mon', hour=9, minute=0)
    
    scheduler.add_job(run_weekly_digest, trigger)
    
    print("Scheduler started. Will run every Monday at 9:00 AM.")
    print("Press Ctrl+C to exit.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped.")
