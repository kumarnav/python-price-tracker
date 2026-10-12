# 📊 Automated Price Tracker & Alert Engine

A robust, lightweight Python utility designed to monitor product pricing changes in real-time, log historical data into an SQLite database, and trigger alerts when items hit target price thresholds.

## 🚀 Features
- **Web Scraping & Parsing:** Uses `BeautifulSoup` and custom HTTP headers to extract pricing data reliably.
- **Historical Data Logging:** Automatically stores timestamps and price points locally using `SQLite` for trend analysis.
- **Instant Alerting Mechanism:** Built-in conditional checks to trigger alerts (easily extendable to Telegram, Discord, or SMTP email notifications).
- **Lightweight & Modular:** Minimal dependencies, fast execution, and zero bloat.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Libraries:** `requests`, `BeautifulSoup4`, `sqlite3`

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/python-price-tracker.git](https://github.com/your-username/python-price-tracker.git)
   cd python-price-tracker