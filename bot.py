import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# ------------------ CONFIG ------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is missing!")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing!")

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# ------------------ COMMANDS ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hello! I am your AI tutor.\n\nAsk me anything about science, tech, or coding!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 Commands:\n"
        "/start - Start bot\n"
        "/help - Help info\n\n"
        "💡 Just send any question!"
    )

# ------------------ AI RESPONSE ------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an intelligent AI tutor specialized in science and technology."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(e)
        await update.message.reply_text("⚠️ Error processing your request.")

# ------------------ MAIN ------------------

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
