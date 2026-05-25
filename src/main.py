import feedparser, json, os, google.generativeai as genai
import requests
from config import *

genai.configure(api_key=GEMINI_API_KEY)

def get_processed_ids():
    if not os.path.exists('data/processed.json'): return []
    with open('data/processed.json', 'r') as f: return json.load(f)

def save_processed_ids(ids):
    with open('data/processed.json', 'w') as f: json.dump(ids, f)

def analyze_with_gemini(news_data):
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
    prompt = f"""Analisis berita berikut: {news_data}. 
    Berikan laporan ringkas: 1. Inti berita, 2. Dampak ke The Fed (Hawkish/Dovish), 3. Dampak ke BTC. 
    Gunakan format Markdown yang rapi."""
    return model.generate_content(prompt).text

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})

def main():
    processed = get_processed_ids()
    new_items = []
    
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]: # Ambil 3 berita terbaru per feed
            if entry.id not in processed:
                analysis = analyze_with_gemini(f"{entry.title} - {entry.summary}")
                send_telegram(f"📢 *{entry.title}*\n\n{analysis}")
                new_items.append(entry.id)
                processed.append(entry.id)
                
    save_processed_ids(processed[-50:]) # Simpan hanya 50 ID terakhir

if __name__ == "__main__":
    main()
