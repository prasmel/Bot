import feedparser, json, os, google.generativeai as genai
import requests
from config import *

genai.configure(api_key=GEMINI_API_KEY)

def get_processed_ids():
    if not os.path.exists('data/processed.json'): return []
    with open('data/processed.json', 'r') as f: 
        try: return json.load(f)
        except: return []

def save_processed_ids(ids):
    with open('data/processed.json', 'w') as f: json.dump(ids, f)

def analyze_with_gemini(news_data):
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
    # Prompt yang diperbarui untuk meminta Sentiment Score
    prompt = f"""Analisis berita berikut secara profesional: {news_data}. 
    Berikan laporan dalam format berikut:
    - Ringkasan: [Inti berita]
    - Dampak The Fed: [Hawkish/Dovish/Neutral]
    - Dampak Kripto: [Potensi pergerakan]
    - Sentiment Score: [Skala -1.0 (Sangat Bearish) sampai 1.0 (Sangat Bullish)]
    - Alasan Skor: [Penjelasan singkat 1 kalimat]
    """
    response = model.generate_content(prompt)
    return response.text

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def main():
    processed = get_processed_ids()
    new_items = []
    
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        # Ambil 2 berita terbaru saja untuk menghindari limit API
        for entry in feed.entries[:2]: 
            if entry.id not in processed:
                try:
                    analysis = analyze_with_gemini(f"{entry.title} - {entry.summary}")
                    message = f"📢 *{entry.title}*\n\n{analysis}\n\n[Baca Selengkapnya]({entry.link})"
                    send_telegram(message)
                    new_items.append(entry.id)
                except Exception as e:
                    print(f"Error processing {entry.id}: {e}")
                
    if new_items:
        processed.extend(new_items)
        save_processed_ids(processed[-50:]) # Simpan riwayat 50 ID terakhir

if __name__ == "__main__":
    main()
