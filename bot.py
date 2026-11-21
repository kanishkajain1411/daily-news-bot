
import os
from datetime import datetime
from urllib.parse import quote_plus

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "").strip()

NEWSPAPER, DATE, LANGUAGE = range(3)

NEWSPAPERS = {
    "bhaskar": "Dainik Bhaskar",
    "patrika": "Rajasthan Patrika",
    "maharashtra": "Maharashtra Times",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Dainik Bhaskar", callback_data="bhaskar")],
        [InlineKeyboardButton("Rajasthan Patrika", callback_data="patrika")],
        [InlineKeyboardButton("Maharashtra Times", callback_data="maharashtra")],
    ]

    await update.message.reply_text(
        "📰 Welcome to Daily Newspaper Bot!\n\n"
        "Select your newspaper:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return NEWSPAPER


async def select_newspaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["newspaper"] = NEWSPAPERS[query.data]

    await query.edit_message_text(
        f"📰 Selected: {context.user_data['newspaper']}\n\n"
        "📅 Enter date in DD-MM-YYYY format.\n"
        "Example: 21-11-2026"
    )

    return DATE


async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date_text = update.message.text.strip()

    try:
        date = datetime.strptime(date_text, "%d-%m-%Y")
        context.user_data["date"] = date.strftime("%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid date!\nPlease enter date in DD-MM-YYYY format.\n"
            "Example: 21-11-2026"
        )
        return DATE

    keyboard = [
        [InlineKeyboardButton("Hindi 🇮🇳", callback_data="Hindi")],
        [InlineKeyboardButton("English 🇬🇧", callback_data="English")],
        [InlineKeyboardButton("Marathi 🇮🇳", callback_data="Marathi")],
    ]

    await update.message.reply_text(
        "🌐 Select newspaper language:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return LANGUAGE


async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    language = query.data
    newspaper = context.user_data["newspaper"]
    date = context.user_data["date"]

    search_query = f"{newspaper} newspaper {date} {language}"

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(search_query)
    )

    keyboard = [
        [InlineKeyboardButton("📖 Find Newspaper", url=search_url)],
        [InlineKeyboardButton("🔄 Start Again", callback_data="restart")],
    ]

    await query.edit_message_text(
        "📰 Your Newspaper Selection\n\n"
        f"Newspaper: {newspaper}\n"
        f"📅 Date: {date}\n"
        f"🌐 Language: {language}\n\n"
        "Click below to find news for your selected date.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return ConversationHandler.END


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Dainik Bhaskar", callback_data="bhaskar")],
        [InlineKeyboardButton("Rajasthan Patrika", callback_data="patrika")],
        [InlineKeyboardButton("Maharashtra Times", callback_data="maharashtra")],
    ]

    await query.edit_message_text(
        "📰 Select your newspaper:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return NEWSPAPER


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled. Use /start to begin again.")
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n\n"
        "/start - Select newspaper\n"
        "/help - Show help\n"
        "/cancel - Cancel selection"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NEWSPAPER: [
                CallbackQueryHandler(select_newspaper, pattern="^(bhaskar|patrika|maharashtra)$")
            ],
            DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_date)
            ],
            LANGUAGE: [
                CallbackQueryHandler(select_language, pattern="^(Hindi|English|Marathi)$")
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conversation)
    app.add_handler(CallbackQueryHandler(restart, pattern="^restart$"))
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
