import requests, time, os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SLOW_COUNTRIES = ["Egypt", "Tunisia", "Algeria", "South Africa", "Greece"]

last_scores = {}
last_reds = {}
last_incidents_count = {}

headers = {"User-Agent": "Mozilla/5.0 (iPhone)", "Accept": "application/json"}

def send(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

send("✅ BOT LIVE - 5 SLOWEST LEAGUES\nEgypt, Tunisia, Algeria, SA, Greece\nGOAL + RED + YELLOW")

while True:
    try:
        live = requests.get("https://www.sofascore.com/api/v1/sport/football/events/live", headers=headers, timeout=10).json()
        for game in live.get("events", []):
            country = game["tournament"]["category"]["name"]
            if country not in SLOW_COUNTRIES: continue
            gid = str(game["id"])
            home = game["homeTeam"]["name"]
            away = game["awayTeam"]["name"]
            league = game["tournament"]["name"]
            hs = game["homeScore"]["current"]
            aws = game["awayScore"]["current"]
            home_red = game["homeScore"].get("redCards", 0)
            away_red = game["awayScore"].get("redCards", 0)
            minute = game["status"].get("description", "")
            
            if gid in last_scores and last_scores[gid] != (hs, aws):
                send(f"⚽ GOAL! {country}\n{league}\n{home} {hs}-{aws} {away}\n{minute}\n💰 BET NOW - 12 sec window!")
            
            if gid in last_reds:
                old_hr, old_ar = last_reds[gid]
                if home_red > old_hr: send(f"🟥 RED CARD {country}\n{league}\n{home} {minute}'")
                if away_red > old_ar: send(f"🟥 RED CARD {country}\n{league}\n{away} {minute}'")
            
            last_scores[gid] = (hs, aws)
            last_reds[gid] = (home_red, away_red)
        time.sleep(3)
    except Exception as e:
        print(e); time.sleep(5)
