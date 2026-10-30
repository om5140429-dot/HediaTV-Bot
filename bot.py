import os
import time
import random
import threading
from flask import Flask
import requests
import yt_dlp
from pyrogram import Client, filters
from internetarchive import upload

# إعداد خادم ويب خفيف عشان Render يفضل مرتاح وما يقفلش البوت
app_web = Flask('')

@app_web.route('/')
def home():
    return "HediaTV-Bot is running 24/7!"

def run_web():
    app_web.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# بدء خادم الويب في خلفية منفصلة
t = threading.Thread(target=run_web)
t.start()

# بيانات البوت من المتغيرات السرية
API_ID = int(os.getenv("API_ID", "36052764"))
API_HASH = os.getenv("API_HASH", "d90e2691d1c4ac4d7f5f4c1175317c32")
BOT_TOKEN = os.getenv("BOT_TOKEN", "9073792660:AAFKr+iG8M6W0tvyI+7yUaCHVQAhWBRjn00")

# مفاتيح Internet Archive السرية
IA_ACCESS_KEY = os.getenv("IA_ACCESS_KEY", "")
IA_SECRET_KEY = os.getenv("IA_SECRET_KEY", "")

app = Client("hedia_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def upload_to_internet_archive(file_path):
    if not IA_ACCESS_KEY or not IA_SECRET_KEY:
        raise Exception("مفاتيح Internet Archive غير موجودة في المتغيرات السرية!")
    
    identifier = f"hediatv_video_{int(time.time())}_{random.randint(1000, 9999)}"
    file_name = os.path.basename(file_path)
    
    upload(
        identifier,
        files=[file_path],
        access_key=IA_ACCESS_KEY,
        secret_key=IA_SECRET_KEY,
        verbose=True
    )
    
    direct_link = f"https://archive.org/download/{identifier}/{file_name}"
    return direct_link

@app.on_message(filters.command("start"))
def start_handler(client, message):
    message.reply_text("🎬 أهلاً بيك يا هندسة في بوت Hedia TV! ابعت لي لينك صفحة التحميل أو الفيديو وهسحبه وأوفر لك رابطه المباشر الدائم فوراً 🚀")

@app.on_message(filters.text & ~filters.command("start"))
def download_handler(client, message):
    # شرط صارم جداً: تجاهل رسائل البوت تماماً، وتجاهل أي نص لا يبدأ بـ http
    if message.from_user.is_bot:
        return
    
    url = message.text.strip()
    if not url.startswith("http"):
        return

    status_msg = message.reply_text("⏳ جاري سحب وتحميل الفيديو من صفحة التحميل سحابياً، ثواني ويكون جاهز...")
    
    # توليد اسم ملف فريد تماماً لكل طلب منعاً لتداخل العمليات
    unique_filename = f"video_{int(time.time())}_{random.randint(1000, 9999)}.mp4"
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': unique_filename,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        status_msg.edit_text("📤 جاري رفع الفيديو على سحابة Internet Archive (دائم وبدون حدود)...")
        
        direct_link = upload_to_internet_archive(unique_filename)
        
        message.reply_text(
            f"✅ **تم تجهيز الفيديو بنجاح يا أسطورة!**\n\n🔗 **الرابط المباشر الدائم:**\n{direct_link}",
            disable_web_page_preview=True
        )
        
        if os.path.exists(unique_filename):
            os.remove(unique_filename)
            
        status_msg.delete()
        
    except Exception as e:
        if os.path.exists(unique_filename):
            os.remove(unique_filename)
        status_msg.edit_text(f"❌ حصل خطأ أثناء المعالجة: {str(e)}")

print("Bot and Web server are running... 🚀")
app.run()
