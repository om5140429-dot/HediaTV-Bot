import os
from pyrogram import Client, filters
import yt_dlp

# بيانات البوت المربطة بيك يا هندسة
API_ID = 36052764
API_HASH = "d90e2691d1c4ac4d7f5f4c1175317c32"
BOT_TOKEN = "9073792660:AAFKr+iG8M6W0tvyI+7yUaCHVQAhWBRjn00"

app = Client("hedia_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_handler(client, message):
    message.reply_text("🎬 أهلاً بيك يا هندسة في بوت Hedia TV! ابعت لي لينك الفيديو وهسحبه وأرفعه لك فوراً وبدون استهلاك مساحة 🚀")

@app.on_message(filters.text & ~filters.command("start"))
def download_handler(client, message):
    url = message.text.strip()
    status_msg = message.reply_text("⏳ جاري سحب وتحميل الفيديو، ثواني ويكون جاهز...")
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        status_msg.edit_text("📤 جاري الرفع على تيليجرام...")
        
        # رفع الفيديو والحصول على رابط مباشر
        sent_msg = client.send_video(
            chat_id=message.chat.id,
            video="video.mp4",
            caption="🎬 اتفضل يا هندسة الفيديو جاهز للتطبيق!"
        )
        
        # مسح الملف من على السيرفر فوراً عشان نحافظ على المساحة (صفر استهلاك)
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
            
        status_msg.delete()
        
    except Exception as e:
        status_msg.edit_text(f"❌ حصل خطأ أثناء المعالجة: {str(e)}")

print("Bot is running and ready... 🚀")
app.run()