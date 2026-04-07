"""
⏰ Weekly Tech Digest - Automation Scheduler
This module handles the recurring execution of the tech digest pipeline.
By default, it is configured to run every Monday at 9:00 AM.
"""

# 💡 CRON ALTERNATIVE (Add to crontab with: crontab -e)
# --------------------------------------------------
# 0 9 * * 1 /usr/bin/python3 /path/to/project/weekly-digest/scheduler.py

import os
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from scraper import get_top_articles
from report_generator import generate_report

# 📝 Logging Configuration
# Errors are persisted to 'output/error.log' for easy debugging of automated runs
os.makedirs("output", exist_ok=True)
logging.basicConfig(
    filename='output/error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_weekly_digest():
    """
    ⚡ The automated task execution sequence.
    This function wraps the entire scraper-to-report pipeline.
    """
    try:
        print(f"[{datetime.now()}] 🔄 Starting automated weekly digest run...")
        
        # 1. Fetch & Rank articles (Top 10)
        articles, total_fetched = get_top_articles(top_n=10)
        
        # 2. Build and save the HTML report
        output_path = generate_report(articles, total_before_dedup=total_fetched)
        
        # 3. Final Logging
        print(f"[{datetime.now()}] ✨ Success: Digest generated with {len(articles)} stories.")
        print(f"📍 Location: {output_path}")
        
    except Exception as e:
        # 🚨 Handle failures gracefully by logging them with a timestamp
        err_msg = f"❌ Pipeline failed: {str(e)}"
        logging.error(err_msg)
        print(f"[{datetime.now()}] {err_msg}. Review output/error.log for stack trace.")
        # We re-raise to allow the scheduler to know the job failed
        raise e

if __name__ == "__main__":
    # 🏁 Scheduler Initialization
    # We use BlockingScheduler as this script is intended to run as a standalone process
    scheduler = BlockingScheduler()
    
    # 🕒 Configuration: Runs every Monday ('mon') at 09:00:00
    trigger = CronTrigger(
        day_of_week='mon', 
        hour=9, 
        minute=0,
        timezone='UTC' # Standardizing on UTC for consistency
    )
    
    # ➕ Add the job to the scheduler
    scheduler.add_job(
        run_weekly_digest, 
        trigger,
        id='weekly_tech_digest_job',
        replace_existing=True
    )
    
    print("🛰️  Automation Engine Started!")
    print("📅 Schedule: Every Monday at 9:00 AM UTC")
    print("🛑 Exit: Press Ctrl+C to terminate.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 Scheduler deactivated successfully.")
