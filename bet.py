import requests
from bs4 import BeautifulSoup
import random
import time
import telebot
from fake_useragent import UserAgent

# Telegram bot setup
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Proxy list (replace with your own)
PROXIES = [
    "http://user:pass@proxy1:port",
    "http://user:pass@proxy2:port",
    "http://user:pass@proxy3:port"
]

# Headers with random User-Agent to avoid detection
ua = UserAgent()
HEADERS = {"User-Agent": ua.random}

# Function to fetch odds from Rollbit
def get_rollbit_odds():
    url = "https://rollbit.com/sports"
    proxy = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}
    response = requests.get(url, headers=HEADERS, proxies=proxy)
    soup = BeautifulSoup(response.text, "html.parser")

    odds = {}  # Store extracted odds here
    # Your scraping logic for Rollbit odds goes here
    return odds

# Function to fetch odds from Thunderpick
def get_thunderpick_odds():
    url = "https://thunderpick.com/sports"
    proxy = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}
    response = requests.get(url, headers=HEADERS, proxies=proxy)
    soup = BeautifulSoup(response.text, "html.parser")

    odds = {}  # Store extracted odds here
    # Your scraping logic for Thunderpick odds goes here
    return odds

# Function to find arbitrage opportunities
def find_arbitrage(rollbit_odds, thunderpick_odds):
    opportunities = []

    # Compare odds for the same event from both sites
    for event in rollbit_odds:
        if event in thunderpick_odds:
            rollbit_best = max(rollbit_odds[event])
            thunderpick_best = max(thunderpick_odds[event])

            # Check if arbitrage exists
            if (1/rollbit_best + 1/thunderpick_best) < 1:
                opportunities.append({
                    "event": event,
                    "rollbit_odds": rollbit_best,
                    "thunderpick_odds": thunderpick_best
                })

    return opportunities

# Function to send Telegram alert
def send_telegram_alert(opportunities):
    for opp in opportunities:
        message = f" Arbitrage Opportunity Found! \n\n" \
                  f"Event: {opp['event']}\n" \
                  f" Rollbit Odds: {opp['rollbit_odds']}\n" \
                  f" Thunderpick Odds: {opp['thunderpick_odds']}\n"
        bot.send_message(TELEGRAM_CHAT_ID, message)

# Main function to run the arbitrage bot
def main():
    while True:
        try:
            rollbit_odds = get_rollbit_odds()
            thunderpick_odds = get_thunderpick_odds()
            opportunities = find_arbitrage(rollbit_odds, thunderpick_odds)

            if opportunities:
                send_telegram_alert(opportunities)

            time.sleep(60)  # Scrape every 60 seconds
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
