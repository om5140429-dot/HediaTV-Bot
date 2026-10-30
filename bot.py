import os
from pyrogram import Client, filters
import yt_dlp

@app.on_message(filters.text & filters.private)
def handle_video_link(client, message):
    url = message.text.strip()
    if url.startswith("http"):
        msg = message.reply("⚡ جاري سحب وتحميل الفيديو سحابياً، ثواني بيكون جاهز...")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'noplaylist': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            # هنا بيكمل كود الرفع السحابي بتاعك (زي Internet Archive)
            message.reply("✅ تم تجهيز الفيديو بنجاح يا أسطورة!")
        except Exception as e:
            message.reply(f"❌ حصل خطأ أثناء المعالجة: {e}")
