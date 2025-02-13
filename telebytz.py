#!/usr/bin/env python3
import os
import re
import json
import time
import random
import feedparser
import requests
from datetime import datetime
from html import unescape
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env
dotenv_path = find_dotenv()
if not dotenv_path:
    raise ValueError("No .env file found in the project directory.")
load_dotenv(dotenv_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env file")

# File to store links of posted messages
POSTED_FILE = "posted_messages.json"

def load_posted_messages():
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_posted_messages(posted):
    with open(POSTED_FILE, "w") as f:
        json.dump(list(posted), f)

posted_messages = load_posted_messages()

# Define feeds for tech and Linux enthusiasts
FEEDS = {
    "Phoronix": "https://www.phoronix.com/rss.php",
    "OMG Ubuntu": "https://www.omgubuntu.co.uk/feed/",
    "TechCrunch": "https://techcrunch.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "Linux Today": "http://www.linuxtoday.com/feed"
}

def get_feed_entries(site, feed_url):
    headers = {'User-Agent': 'Mozilla/5.0 (LibertyBot/1.0)'}
    feed = feedparser.parse(feed_url, request_headers=headers)
    if feed.bozo:
        print(f"Warning: {site} feed parsing error: {feed.bozo_exception}")
    return feed.entries

def fetch_all_entries():
    entries = []
    for site, feed_url in FEEDS.items():
        feed_entries = get_feed_entries(site, feed_url)
        if feed_entries:
            print(f"Fetched {len(feed_entries)} entries from {site}")
            for entry in feed_entries:
                entry["site"] = site
                entries.append(entry)
        else:
            print(f"No entries found for {site}")
    return entries

def extract_image(entry):
    if "media_content" in entry:
        for media in entry.media_content:
            if "url" in media:
                return media["url"]
    if "links" in entry:
        for link in entry.links:
            if link.get("rel") == "enclosure" and "image" in link.get("type", ""):
                return link.get("href")
    return None

def clean_html_tags(text):
    # Remove <p> and <img> tags (Telegram doesn't allow these in HTML mode)
    text = re.sub(r"</?p[^>]*>", "", text)
    text = re.sub(r"<img[^>]*>", "", text)
    return unescape(text)

def format_message(entry):
    title = entry.get("title", "No Title")
    link = entry.get("link", "")
    raw_summary = entry.get("summary", "")
    summary = clean_html_tags(raw_summary)
    site = entry.get("site", "")
    # Use double quotes for the <a> tag per Telegram's HTML mode requirements
    return f"<b>{title}</b> ({site})\n{summary}\n<a href=\"{link}\">Read more</a>"

def post_to_telegram(message, image_url=None):
    if image_url:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": message,
            "photo": image_url,
            "parse_mode": "HTML"
        }
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        print("Telegram message posted successfully!")
    except Exception as e:
        print(f"Error posting to Telegram: {e}")

def main_loop():
    global posted_messages
    while True:
        entries = fetch_all_entries()
        # Filter out entries already posted (by link)
        new_entries = [entry for entry in entries if entry.get("link", "") not in posted_messages]
        if new_entries:
            # Sort entries by publication date (if available) and pick the latest
            def get_pub_date(entry):
                if 'published_parsed' in entry and entry.published_parsed:
                    return datetime(*entry.published_parsed[:6])
                return datetime.min
            new_entries.sort(key=get_pub_date, reverse=True)
            entry = new_entries[0]
            message = format_message(entry)
            image_url = extract_image(entry)
            post_to_telegram(message, image_url)
            posted_messages.add(entry.get("link", ""))
            save_posted_messages(posted_messages)
        else:
            print("No new entries available to post.")
        # Wait for a random delay between 2 and 3 hours
        delay = random.randint(2 * 3600, 3 * 3600)
        print(f"Sleeping for {delay/3600:.2f} hours...")
        time.sleep(delay)

if __name__ == "__main__":
    main_loop()
