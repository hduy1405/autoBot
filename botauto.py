import os
import yt_dlp
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# ===== FAKE WEB SERVER (CHO RENDER) =====
def run_web():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

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
    # chạy web fake song song
    threading.Thread(target=run_web).start()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("dl", dl))

    print("🤖 Bot đang chạy...")
    app.run_polling()