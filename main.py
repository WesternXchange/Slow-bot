import os
import time
import requests
from flask import Flask
from threading import Thread
from datetime import datetime

# === 1. KEEP RENDER ALIVE (FIXES YOUR FAIL) ===
app = Flask(__name__)

@app.route('/')
def home():
    return "BOT LIVE - 5 SLOWEST LEAGUES - EGYPT, TUNISIA, ALGERIA, SA, GREECE"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web, daemon=True).start()

# === 2. YOUR BOT CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ONLY these 5 leagues will ever send - NOTHING ELSE
ALLOWED_LEAGUES_KEYWORDS = [
    "egypt", 
    "tunisia", 
    "algeria", 
    "south africa", "psl", "south-africa",
    "greece"
]

def is_allowed_league(league_name: str):
    if not league_name:
        return False
    league_name = league_name.lower()
    return any(k in league_name for k in ALLOWED_LEAGUES_KEYWORDS)

def send_telegram(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing BOT_TOKEN or CHAT_ID")
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
        r = requests.post(url, json=payload, timeout=15)
        print(f"Telegram sent: {r.status_code} - {text[:50]}")
    except Exception as e:
        print(f"Send error: {e}")

# === 3. BOT START ===
time.sleep(3)
send_telegram("✅ *BOT LIVE - 5 SLOWEST LEAGUES*\n\nFilter Active: Egypt, Tunisia, Algeria, SA, Greece only\nRender: ONLINE\nReady to send signals!")

print("Bot started, entering loop...")

# === 4. YOUR STRATEGY LOOP - REPLACE THIS WITH YOUR SPORTMONKS LOGIC ===
# This is a safe keep-alive loop. Put your real checking code inside.
while True:
    try:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] Bot heartbeat - checking 5 leagues only...")
        
        # --- EXAMPLE: How to use the filter ---
        # league_from_api = "Egypt Premier League"
        # if is_allowed_league(league_from_api):
        #     send_telegram("⚽ GOAL - Egypt...")
        # else:
        #     print(f"Skipped league: {league_from_api}")

        time.sleep(60)  # Check every 60 seconds

    except Exception as e:
        print(f"Loop error: {e}")
        time.sleep(10)
