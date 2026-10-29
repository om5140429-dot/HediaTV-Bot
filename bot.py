import os
from pyrogram import Client, filters
import yt_dlp
from flask import Flask
import threading
import requests

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

app = Client("hedia_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def upload_to_catbox(file_path):
    """دالة لرفع الفيديو تلقائياً على Catbox.moe وإرجاع الرابط المباشر"""
    url = "https://catbox.moe/user/api.php"
    with open(file_path, 'rb') as f:
        files = {'fileToUpload': f}
        data = {'reqtype': 'fileupload'}
        response = requests.post(url, data=data, files=files)
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception("فشل الرفع على سحابة Catbox")

@app.on_message(filters.command("start"))
def start_handler(client, message):
    message.reply_text("🎬 أهلاً بيك يا هندسة في بوت Hedia TV! ابعت لي لينك الفيديو وهسحبه وأوفر لك رابطه المباشر الدائم فوراً 🚀")

@app.on_message(filters.text & ~filters.command("start"))
def download_handler(client, message):
    url = message.text.strip()
    status_msg = message.reply_text("⏳ جاري سحب وتحميل الفيديو سحابياً، ثواني ويكون جاهز...")
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        status_msg.edit_text("📤 جاري توليد الرابط المباشر الدائم...")
        
        # رفع الفيديو لـ Catbox والحصول على الرابط المباشر
        direct_link = upload_to_catbox("video.mp4")
        
        # إرسال الرابط المباشر فقط للمستخدم بدون إعادة إرسال الملف
        message.reply_text(
            f"✅ **تم تجهيز الفيديو بنجاح يا أسطورة!**\n\n🔗 **الرابط المباشر الدائم:**\n{direct_link}",
            disable_web_page_preview=True
        )
        
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
            
        status_msg.delete()
        
    except Exception as e:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
        status_msg.edit_text(f"❌ حصل خطأ أثناء المعالجة: {str(e)}")

print("Bot and Web server are running... 🚀")
app.run()
