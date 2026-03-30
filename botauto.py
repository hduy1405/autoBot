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

# ===== DOWNLOAD (FIX FULL) =====
def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best[height<=480]',
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': 'mp4',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return "video.mp4"

    except Exception as e:
        print("❌ yt-dlp error:", e)
        return None

# ===== COMMAND =====
async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("❌ Dùng: /dl link")
            return

        url = context.args[0]

        await update.message.reply_text("📥 Đang tải...")

        file_path = download_video(url)

        if not file_path or not os.path.exists(file_path):
            await update.message.reply_text("❌ Không tải được video (link lỗi hoặc bị chặn)")
            return

        size = os.path.getsize(file_path) / (1024 * 1024)
        print(f"📦 File size: {size:.2f} MB")

        if size > 49:
            await update.message.reply_text("❌ Video quá nặng (>50MB)")
            os.remove(file_path)
            return

        with open(file_path, 'rb') as f:
            await update.message.reply_video(video=f)

        os.remove(file_path)

    except Exception as e:
        print("❌ ERROR:", e)
        await update.message.reply_text("❌ Lỗi tải video")

# ===== MAIN =====
if __name__ == "__main__":
    # 🔥 tránh conflict (reset webhook)
    import requests
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
    except:
        pass

    # chạy web fake
    threading.Thread(target=run_web, daemon=True).start()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("dl", dl))

    print("🤖 Bot đang chạy...")
    app.run_polling()