# Implementation Plan - Weekly Tech Digest Scraper

This plan outlines the steps to complete the Weekly Tech Digest Scraper project as described in `prompt.md`.

## Phase 1: Project Setup and Scraper (Prompt 1)
- [ ] Create directory structure `weekly-digest/`.
- [ ] Create `requirements.txt` with pinned dependencies.
- [ ] Create `scraper.py` with:
    - `fetch_hackernews(limit=20)`
    - `fetch_devto(limit=20)`
    - `calculate_engagement(article)`
    - `deduplicate(articles, threshold=80)`
    - `get_top_articles(top_n=10)`
- [ ] Create `output/.gitkeep` and `templates/`.
- [ ] Create a placeholder `README.md`.

## Phase 2: Report Generation (Prompt 2)
- [ ] Create `templates/digest.html` (Jinja2 template with CSS).
- [ ] Create `report_generator.py` with:
    - `generate_report(articles, output_path, total_before_dedup)`
    - `if __name__ == "__main__":` block for testing.

## Phase 3: Scheduler and Final Polish (Prompt 3)
- [ ] Create `scheduler.py` with:
    - `run_weekly_digest()`
    - APScheduler `BlockingScheduler` with `CronTrigger`.
- [ ] Update `get_top_articles` in `scraper.py` to return `(articles, total_fetched)`.
- [ ] Update `report_generator.py` to handle the new return type.
- [ ] Implement error handling and logging to `output/error.log`.
- [ ] Write the final `README.md`.

## Phase 4: Git Workflow
- [ ] Create a new branch `feat/weekly-tech-digest`.
- [ ] Stage and commit all changes.
- [ ] Push the branch.
- [ ] Merge the branch into `main`.
