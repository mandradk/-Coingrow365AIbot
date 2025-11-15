import os
import time
import requests

TOKEN = os.environ.get("TOKEN")  # Token Render ke environment se ayega
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

PRICE_API = "https://api.coingecko.com/api/v3/simple/price"

def get_updates(offset=None):
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    try:
        resp = requests.get(BASE_URL + "/getUpdates", params=params, timeout=35)
        return resp.json()
    except Exception as e:
        print("Error in get_updates:", e)
        return {}

def send_message(chat_id, text):
    try:
        requests.post(
            BASE_URL + "/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=10,
        )
    except Exception as e:
        print("Error in send_message:", e)

def get_price(symbol="btc"):
    params = {"ids": symbol, "vs_currencies": "usd"}
    try:
        r = requests.get(PRICE_API, params=params, timeout=10)
        data = r.json()
        if symbol in data:
            return data[symbol]["usd"]
        return None
    except Exception as e:
        print("Error in get_price:", e)
        return None

def handle_start(chat_id):
    msg = (
        "👋 Welcome to *Coingrow365 AI Bot!*\n"
        "Your Smart Crypto Knowledge Partner.\n\n"
        "Commands:\n"
        "• /price BTC\n"
        "• /price ETH\n"
        "• /help\n\n"
        "Coingrow365 — Learn. Analyze. Grow."
    )
    send_message(chat_id, msg)

def handle_help(chat_id):
    msg = "🧾 Help:\nUse: `/price BTC` or `/price ETH`.\nMore tools coming soon."
    send_message(chat_id, msg)

def handle_price(chat_id, text):
    parts = text.split()
    if len(parts) < 2:
        send_message(chat_id, "Usage: /price BTC")
        return
    symbol = parts[1].lower()
    price = get_price(symbol)
    if price:
        send_message(
            chat_id,
            f"{symbol.upper()} Price:\n• {price} USD\n\nCoingrow365 — Learn. Analyze. Grow.",
        )
    else:
        send_message(chat_id, "Coin not found!")

def main():
    print("Bot Started on Render...")
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        if "result" in updates:
            for item in updates["result"]:
                last_update_id = item["update_id"] + 1
                msg = item.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id", "")

                if not text or not chat_id:
                    continue

                t = text.lower()

                if t.startswith("/start"):
                    handle_start(chat_id)
                elif t.startswith("/help"):
                    handle_help(chat_id)
                elif t.startswith("/price"):
                    handle_price(chat_id, text)

        time.sleep(1)

if __name__ == "__main__":
    main()
