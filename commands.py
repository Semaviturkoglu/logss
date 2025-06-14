# commands.py
import requests
import datetime
import random
import string

async def komutlar(update, arg_text, cmd):
    if cmd == "start":
        await update.message.reply_text("naber nasılsın burnun kapıya kısılsın hayat nasıl gidiyor kim çağırdı beni")
    elif cmd == "help":
        await update.message.reply_text("""🧠 Komut Listesi:
$start → Botu başlatır.
$help → Tüm komutları gösterir.
$sor <metin> → Yapay zekadan yanıt al.
$banabirkodyaz <konu> → Otomatik kod yazdırır.
$kripto <coin> → Coin fiyatını gösterir.
$havadurumu <şehir> → Hava durumu bilgisi getirir.
$sondurum türkiye → Türkiye'de siyasi hava ☕
$rastgele → 1-100 arasında sayı üretir.
$kelimesay → Cümledeki kelime sayısını gösterir.
$harfler → Harf sayısını verir.
$emoji → Emoji koleksiyonu gönderir.
$zaman / $tarih → Güncel saat/tarih verir.
$kahvefalı → Eğlencelik fal verir.
$şifreüret → Rastgele güçlü şifre oluşturur.
$log → Kayıtları sadece admin görebilir.
""")
    elif cmd == "rastgele":
        await update.message.reply_text(f"Rastgele sayı: {random.randint(1, 100)}")
    elif cmd == "kelimesay":
        await update.message.reply_text(f"Kelime sayısı: {len(arg_text.split())}")
    elif cmd == "harfler":
        await update.message.reply_text(f"Harf sayısı: {len(arg_text.replace(' ', ''))}")
    elif cmd == "emoji":
        await update.message.reply_text("😎🚀🔥💻🧠✨")
    elif cmd == "zaman":
        await update.message.reply_text(f"Şu an saat: {datetime.datetime.now().strftime('%H:%M:%S')}")
    elif cmd == "tarih":
        await update.message.reply_text(f"Bugün: {datetime.date.today().strftime('%d.%m.%Y')}")
    elif cmd == "kahvefalı":
        await update.message.reply_text(random.choice([
            "Bugün güzel haberler alacaksın.",
            "Dikkat et kıskanan biri var 😏",
            "Para geliyor, hazır ol!"
        ]))
    elif cmd == "şifreüret":
        await update.message.reply_text("🔐 " + ''.join(random.choices(string.ascii_letters + string.digits, k=12)))
    else:
        return False  # Bu komutu burada tanımıyoruz
    return True
