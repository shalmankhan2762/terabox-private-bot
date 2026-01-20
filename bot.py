import os
import requests
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    await update.message.reply_text("⬇️ Downloading...")

    try:
        # Simple unofficial API (may change)
        api = "https://terabox-downloader.vercel.app/api"
        r = requests.get(api, params={"url": link}, timeout=60).json()

        if not r.get("downloadUrl"):
            raise Exception("Failed to get download link")

        video = requests.get(r["downloadUrl"], timeout=60).content

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as f:
            f.write(video)
            path = f.name

        await update.message.reply_video(video=open(path, "rb"))
        os.remove(path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
