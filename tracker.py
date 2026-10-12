import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Database setup
DB_NAME = "prices.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            price REAL,
            timestamp TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def track_price(product_name, url, target_price):
    init_db()

    # Headers to mimic a real browser request
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # NOTE: Update this selector based on the target website's HTML structure
        # Example using a generic class name often found on e-commerce sites
        price_element = soup.find("span", {"class": "a-price-whole"})

        if not price_element:
            print(
                "[-] Could not find price element. Check CSS selectors or site structure."
            )
            return

        # Clean the price string (remove commas, currency symbols, etc.)
        price_text = (
            price_element.text.replace(",", "")
            .replace("₹", "")
            .replace("$", "")
            .strip()
        )
        current_price = float(price_text)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to SQLite
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO price_history (product_name, price, timestamp) VALUES (?, ?, ?)",
            (product_name, current_price, timestamp),
        )
        conn.commit()
        conn.close()

        print(
            f"[+] [{timestamp}] Checked {product_name}: Current Price = {current_price}"
        )

        # Alert logic
        if current_price <= target_price:
            print(
                f"🚨 ALERT! {product_name} dropped to {current_price} (Target: {target_price})!"
            )
            # You can hook a Telegram Bot API or Discord Webhook here

    except Exception as e:
        print(f"[-] Error tracking price: {e}")


if __name__ == "__main__":
    # Let's test with a real public webpage or a simple site
    PRODUCT = "Example Book"
    PRODUCT_URL = (
        "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    TARGET_PRICE = 60.00

    print(f"[*] Starting price tracker for: {PRODUCT}")

    # For books.toscrape.com, the price class is 'price_color'
    # Let's quickly adjust how we find the element for this test:
    import requests
    from bs4 import BeautifulSoup

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Target the price element on books.toscrape.com
    price_element = soup.find("p", {"class": "price_color"})

    if price_element:
        price_text = (
            price_element.text.replace("£", "").replace("Â", "").strip()
        )
        print(
            f"[+] Success! Found price for {PRODUCT}: £{float(price_text):.2f}"
        )
    else:
        print("[-] Price element not found.")