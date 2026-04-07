# 🚀 Weekly Tech Digest Scraper 📰✨

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/kalviumcommunity/weekly-digest/graphs/commit-activity)

> **Stop wasting time manually browsing!** Automate your Monday mornings with a perfectly curated tech digest delivered straight to your browser. 🤖💼

---

## 🌟 Overview

The **Weekly Tech Digest Scraper** is an intelligent automation tool designed for media professionals and tech enthusiasts. It aggregates the most trending stories from **Hacker News** and **DEV.to**, ranks them using a weighted engagement algorithm, and generates a premium HTML report. 

No more inconsistent manual picks—just pure, data-driven insights every Monday at 9:00 AM. 📈

### 🎯 Key Features
- **📥 Dual-Source Aggregation**: Fetches the top 20 stories from both Hacker News and DEV.to.
- **⚖️ Weighted Scoring**: Calculates priority using: `(Votes × 1.0) + (Comments × 1.5)`.
- **🧹 Smart Deduplication**: Uses fuzzy string matching (>80% similarity) to eliminate cross-platform duplicates.
- **🎨 Premium HTML Reports**: Beautifully designed template with platform-specific branding.
- **⏰ Set-and-Forget Automation**: Integrated APScheduler and Cron support.

---

## 🛠️ Project Architecture

```text
weekly-digest/
├── scraper.py           # 🏎️ The Engine: Data extraction & processing
├── report_generator.py   # 🎨 The Artist: HTML template rendering
├── scheduler.py          # 🕒 The Watchman: Automation & scheduling
├── templates/
│   └── digest.html       # 🏗️ The Blueprint: Premium Jinja2 template
├── output/
│   ├── weekly_digest.html # 📄 The Result: A sample output file
│   └── error.log          # 🚨 The Blackbox: Error tracking
├── requirements.txt      # 📦 The Gear: Project dependencies
└── README.md             # 📖 The Map: This guide
```

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/kalviumcommunity/weekly-digest.git
cd weekly-digest
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run Manually (Instant Results! ⚡)
```bash
python report_generator.py
```
Check the results in `output/weekly_digest.html`!

---

## ⏰ Automation & Scheduling

### Option A: Built-in Scheduler (Recommended)
The project comes with a Python-based scheduler that stays active and triggers the run every Monday.
```bash
python scheduler.py
```

### Option B: Linux/macOS Cron
Add this to your crontab (`crontab -e`) for a lightweight, system-level schedule:
```bash
0 9 * * 1 /usr/bin/python3 /path/to/project/weekly-digest/scheduler.py
```

---

## 📊 Engagement Logic

We believe that **discussion** is a stronger signal than passive upvoting.
Our formula reflects this philosophy:

| Metric | Weight | Reason |
| :--- | :--- | :--- |
| **Votes** | `1.0` | Base community interest. |
| **Comments** | `1.5` | High-intent interaction & discussion. |

---

## 📸 Sample Preview
The generated report features:
- 🥇 Rank identifiers for the Top 10 stories.
- 🏷️ Dynamic platform badges (Orange for HN, Purple for DEV).
- 💬 Interaction stats at a glance.
- 🏷️ Tag pills for quick topic identification.

*(Check out `output/weekly_digest.html` for the full live experience!)*

---

## 🤝 Contributing & Docs
Want to help? Check out our [Contributing Guide](docs/CONTRIBUTING.md)!
For project history and implementation details, see our [Project Docs](docs/PROJECT_README.md).

---

## 📜 License
This project is licensed under the MIT License - see the `LICENSE` file for details.

---
**Made with ❤️ for the Developer Community.**
