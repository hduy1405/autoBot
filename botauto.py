import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8753803503:AAFrgbdiJqWVzizGHfCtHME--sNMNJLgFs8"

# ===== DOWNLOAD =====
def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[height<=720]'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# ===== COMMAND /dl =====
async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = context.args[0]

        await update.message.reply_text("📥 Đang tải...")

        file_path = download_video(url)

        await update.message.reply_video(video=open(file_path, 'rb'))

        os.remove(file_path)

    except:
        await update.message.reply_text("❌ Sai cú pháp. Dùng: /dl link")

# ===== MAIN =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("dl", dl))

print("🤖 Bot đang chạy...")
app.run_polling()