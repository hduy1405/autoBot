import os
import yt_dlp
from telegram.ext import Updater, CommandHandler

TOKEN = os.getenv("TOKEN")

def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[height<=720]'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def dl(update, context):
    try:
        if not context.args:
            update.message.reply_text("❌ Dùng: /dl link")
            return

        url = context.args[0]

        update.message.reply_text("📥 Đang tải...")

        file_path = download_video(url)

        update.message.reply_video(video=open(file_path, 'rb'))

        os.remove(file_path)

    except Exception as e:
        print("❌", e)
        update.message.reply_text("❌ Lỗi tải video")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("dl", dl))

    updater.start_polling()
    print("🤖 Bot đang chạy...")
    updater.idle()

if __name__ == "__main__":
    main()