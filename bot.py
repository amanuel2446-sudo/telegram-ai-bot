from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os

# 🔐 GET TOKENS FROM ENVIRONMENT (SAFE)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

user_lang = {}


# 🌍 START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [["English 🇬🇧", "Amharic 🇪🇹"]]

    await update.message.reply_text(
        "🌍 Choose language / ቋንቋ ይምረጡ:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


# 🤖 AI FUNCTION
def ask_ai(prompt):
    url = "https://api.openai.com/v1/responses"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "input": prompt,
        "max_output_tokens": 200
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["output"][0]["content"][0]["text"]
        else:
            return "AI Error: " + response.text

    except Exception as e:
        return "Request failed: " + str(e)


# 💬 MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_chat.id

    # 🌐 Language selection
    if text == "English 🇬🇧":
        user_lang[user_id] = "en"
        await update.message.reply_text("English selected ✅")
        return

    if text == "Amharic 🇪🇹":
        user_lang[user_id] = "am"
        await update.message.reply_text("አማርኛ ተመርጧል ✅")
        return

    lang = user_lang.get(user_id, "en")

    if lang == "am":
        prompt = "Answer in Amharic: " + text
    else:
        prompt = "Answer in English: " + text

    try:
        await update.message.chat.send_action(action="typing")

        reply = ask_ai(prompt)

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Error: " + str(e))


# 🚀 MAIN FUNCTION
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


# ▶ RUN
if __name__ == "__main__":
    main()
