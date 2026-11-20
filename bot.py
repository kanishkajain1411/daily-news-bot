import os
import feedparser
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "").strip()

print("Token loaded:", bool(TOKEN))
print("Token length:", len(TOKEN))
RSS_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Daily News Bot!\n\n"
        "📰 Get the latest news anytime.\n\n"
        "Use /news to read today's headlines."
    )


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📰 Fetching latest news...")

    try:
        feed = feedparser.parse(RSS_URL)

        if not feed.entries:
            await update.message.reply_text(
                "Sorry, news is unavailable right now."
            )
            return

        message = "🌍 Latest World News\n\n"

        for i, entry in enumerate(feed.entries[:5], start=1):
            message += f"{i}. {entry.title}\n"
            message += f"{entry.link}\n\n"

        await update.message.reply_text(message)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text(
            "Something went wrong while fetching news."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/news - Get latest World News\n"
        "/help - Show help"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("help", help_command))

    port = int(os.environ.get("PORT", 10000))
    external_url = os.environ.get("RENDER_EXTERNAL_URL")

    print("Bot is starting in webhook mode...")

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="telegram",
        webhook_url=f"{external_url}/telegram",
    )


if __name__ == "__main__":
    main()