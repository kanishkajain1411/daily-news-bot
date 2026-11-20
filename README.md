# Daily Newspaper Telegram Bot

A Python-based Telegram bot that fetches the latest World News headlines using an RSS feed from BBC News.

## Features

- Fetches latest World News.
- Provides 5 latest headlines.
- Telegram commands: /start, /news and /help.
- Uses RSS feeds.
- Built using Python.

## Technologies Used

- Python
- Telegram Bot API
- Feedparser
- python-telegram-bot
- Git & GitHub

## Setup & Installation

1. Clone the repository:

   git clone https://github.com/kanishkajain1411/daily-news-bot.git

2. Navigate to project folder:

   cd daily-news-bot

3. Create a virtual environment:

   python -m venv venv

4. Activate virtual environment:

   venv\Scripts\activate

5. Install dependencies:

   pip install python-telegram-bot feedparser python-dotenv

6. Create a .env file and add your Telegram bot token:

   BOT_TOKEN=your_bot_token

7. Run the bot:

   python bot.py

## Commands

/start - Start the bot

/news - Get latest World News

/help - Show available commands

## News Source

BBC News RSS Feed:
https://feeds.bbci.co.uk/news/world/rss.xml

## Author

Kanishka Jain
