# Weekly Tech Digest Scraper

## Overview
An automated news digest tool that aggregates top technology articles from Hacker News and DEV.to. It calculates engagement scores, deduplicates similar content using fuzzy matching, and generates a beautiful HTML report every week.

## Setup
```bash
git clone <repo-url>
cd weekly-digest
pip install -r requirements.txt
```

## Run manually
```bash
python report_generator.py
```
Open `output/weekly_digest.html` in a browser to view the report.

## Run on a schedule
```bash
python scheduler.py
```
The scheduler runs the digest every Monday at 9am and stays alive until interrupted with Ctrl+C.

## Cron alternative
Add the following entry to your crontab using `crontab -e`:
```bash
0 9 * * 1 /usr/bin/python3 /path/to/project/weekly-digest/scheduler.py
```
*Note: Ensure you replace `/path/to/project/` with the actual absolute path to the project directory.*

## Output files
- `output/weekly_digest.html`: The generated HTML report with top tech articles.
- `output/error.log`: Log file containing error details if the pipeline fails.

## Sample output
See `output/weekly_digest.html` for a sample output from a real run.

## Engagement score formula
The tool uses a weighted engagement formula to prioritize high-quality discussions:
`score = (votes * 1.0) + (comments * 1.5)`

This weighting favors articles with active discussions (comments) over those with just upvotes.
