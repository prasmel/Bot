import os

# Gunakan os.getenv untuk mengambil data dari GitHub Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_URLS = [
    "https://www.federalreserve.gov/feeds/press_all.xml",
    "https://cointelegraph.com/rss"
]
