import os
import logging
from pyrogram import Client, filters
import yt_dlp
from internetarchive import upload, get_item

# إعدادات البوت الأساسية من متغيرات البيئة
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
IA_ACCESS_KEY = os.environ.get("IA_ACCESS_KEY", "")
IA_SECRET_KEY = os.environ.get("IA_SECRET_KEY", "")

app = Client("HediaTVBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_cmd(client, message):
    message.reply("أهلاً بيك يا أسطورة! ابعث لي رابط الفيديو وسأقوم بتحميله ورفعه لك فوراً. 🦾")

@app.on_message(filters.text & filters.private)
def download_and_upload(client, message):
    url = message.text.strip()
    if not url.startswith("http"):
        return

    m = message.reply("⚡ جاري معالجة وسحب الفيديو، ثواني ويكون عندك...")
    
    output_filename = "video.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_filename,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_filename):
            try:
                m.edit("📤 جاري رفع الملف على أرشيف السحاب...")
            except:
                pass
            
            # رفع الملف على Internet Archive بالاسم الثابت والنظيف
            identifier = f"hediatv-{os.urandom(3).hex()}"
            safe_filename = "video.mp4"
            s3_access = {'access_key': IA_ACCESS_KEY, 'secret_key': IA_SECRET_KEY}
            
            r = upload(identifier, files=[(output_filename, safe_filename)], metadata={'mediatype': 'movies', 'title': 'HediaTV Download'}, **s3_access)
            
            if r[0].status_code == 200:
                direct_link = f"https://archive.org/download/{identifier}/{safe_filename}"
                message.reply(f"✅ تم الرفع بنجاح يا فنان!\n\n🔗 **الرابط المباشر:**\n{direct_link}")
            else:
                message.reply("❌ حدث خطأ أثناء الرفع على الأرشيف.")
                
            if os.path.exists(output_filename):
                os.remove(output_filename)
        else:
            message.reply("❌ فشل تحميل الملف.")
    except Exception as e:
        message.reply(f"❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    app.run()
