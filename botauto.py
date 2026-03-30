import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# ===== DOWNLOAD =====
def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[height<=720]'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# ===== COMMAND =====
async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("❌ Dùng: /dl link")
            return

        url = context.args[0]

        await update.message.reply_text("📥 Đang tải...")

        file_path = download_video(url)

        with open(file_path, 'rb') as f:
            await update.message.reply_video(video=f)

        os.remove(file_path)

    except Exception as e:
        print("❌", e)
        await update.message.reply_text("❌ Lỗi tải video")

# ===== MAIN =====
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("dl", dl))

    print("🤖 Bot đang chạy...")
    app.run_polling()