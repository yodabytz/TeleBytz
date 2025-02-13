# TeleBytz

TeleBytz is a Telegram bot that aggregates the latest news from technology and Linux feeds and posts a curated update to your Telegram channel at random intervals. It fetches articles from multiple sources, filters out duplicates, and posts the most recent update (with image support if available).

## Features

- **Multi-Feed Aggregation:** Fetches entries from a curated list of tech and Linux feeds.
- **Duplicate Filtering:** Prevents reposting the same article by tracking posted links.
- **Automatic Posting:** Posts the latest article to Telegram at random intervals (between 2 and 3 hours).
- **HTML Cleaning:** Formats messages for Telegram's HTML parse mode.
- **Image Extraction:** Attempts to extract and post images along with the text when available.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/TeleBytz.git
   cd TeleBytz


## (Optional) Create a Virtual Environment:
```
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies:
```
pip install -r requirements.txt

```
## Configure Environment Variables:
In your provided .env file, change your token and chat-id
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```
## Usage
Run the bot with:
```
python telebytz.py
```

## Feeds
TeleBytz currently includes feeds from the following sources:

Phoronix: https://www.phoronix.com/rss.php
OMG Ubuntu: https://www.omgubuntu.co.uk/feed/
TechCrunch: https://techcrunch.com/feed/
Wired: https://www.wired.com/feed/rss
Ars Technica: https://feeds.arstechnica.com/arstechnica/index
Linux Today: http://www.linuxtoday.com/feed
Feel free to modify the FEEDS dictionary in liberty.py to add or remove sources.

## Contributing
Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
