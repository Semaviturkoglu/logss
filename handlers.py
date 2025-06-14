import requests
import json
import random
import datetime
import string
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "https://llm.chutes.ai/v1/chat/completions"
API_KEY = "cpk_8937ee9e55f24cb2abd8834eaeddcf7d.de6674855b555af8973f338eb5a2f634.slMtHr0pAQa1AVA3HMszSpTcmRxTdATH"
DEFAULT_MODEL = "cognitivecomputations/Dolphin3.0-Mistral-24B"

ADMIN_USERNAMES = ["semaviturkoglu", "Trackownerr", "hicfarketmezlan"]  # @ olmadan yaz admins

LOG_FILE = "log.json"

# Mesaj ve kullanıcı adlarını loglamak için
def log_message(username: str, message: str):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append({"user": username, "message": message})

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def send_to_llm(update: Update, user_prompt: str, model_name: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": user_prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        res = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        result = res.json()
        reply = result["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("API’den cevap alamadım kanka: " + str(e))


async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    user = update.message.from_user
    username = user.username or user.first_name or "Anonim"

    # Logla
    log_message(username, msg)

    if not msg.startswith("$"):
        return

    cmd, *args = msg[1:].split(" ", 1)
    arg_text = args[0] if args else ""

    # Komutlar
    if cmd == "start":
        await update.message.reply_text("naber nasılsın burnun kapıya kısılsın hayat nasıl gidiyor kim çağırdı beni")

    elif cmd == "sor":
        if not arg_text:
            await update.message.reply_text("Bir şey yaz da sorayım 😅 Örnek: `$sor bana bir hikaye anlat`")
        else:
            await send_to_llm(update, arg_text, DEFAULT_MODEL)

    elif cmd == "banabirkodyaz":
        if not arg_text:
            await update.message.reply_text("Ne yazacağımı da yazaydın 😒 Örnek: $banabirkodyaz discord botu")
        else:
            await send_to_llm(update, arg_text, DEFAULT_MODEL)

    elif cmd == "kripto":
        if not arg_text:
            await update.message.reply_text("Coin yaz mesela: $kripto bitcoin")
        else:
            try:
                res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={arg_text.lower()}&vs_currencies=usd")
                price = res.json()[arg_text.lower()]["usd"]
                await update.message.reply_text(f"{arg_text.capitalize()} şu an: ${price}")
            except:
                await update.message.reply_text("Coin bulunamadı ya da API çöktü 👀")

    elif cmd == "havadurumu" or cmd == "hava":
        if not arg_text:
            await update.message.reply_text("Bir il adı yaz kanka, örnek: $havadurumu Adana")
        else:
            try:
                res = requests.get(f"https://wttr.in/{arg_text}?format=3")
                await update.message.reply_text(res.text)
            except:
                await update.message.reply_text("Hava durumu alınamadı 🌪️")

    elif cmd == "help":
        await update.message.reply_text("""📜 Komutlar:
$start → Botu başlatır.
$banabirkodyaz <metin> → Kod yazdırır.
$kripto <coin_adı> → Coin fiyatı getirir.
$havadurumu <il> → Hava durumunu gösterir.
$sor <metin> → Yapay zeka yanıtı.
$sondurum <ülke> → Siyasi şaka ve yorum yapar (sadece Türkiye için).
$rastgele → 1-100 arası sayı verir.
$tersyaz <metin> → Metni ters yazar.
$buyukharf <metin> → Metni büyütür.
$kucukharf <metin> → Metni küçültür.
$kelimesay <metin> → Kelime sayısı verir.
$harfler <metin> → Harf sayısı verir.
$terskelime <metin> → Kelime sırasını ters çevirir.
$kahvefalı → Kahve falı söyler.
$doğumgünü → Doğum günü kutlar.
$sağlık → Sağlık tavsiyesi verir.
$günaydın → Günaydın der.
$iyiakşamlar → İyi akşamlar der.
$şifreüret → Rastgele şifre üretir.
$emoji → Emoji gönderir.
$kurs → Güncel döviz fiyatı verir.
$selam → Selam verir.
$zaman → Şu an saat.
$tarih → Bugünün tarihi.
$fakto <sayı> → Faktöriyel hesaplar.
$sondurum <ülke> → Siyasi şaka yapar (yalnız Türkiye).
$log → Adminlere özel mesaj logu.
""")

    elif cmd == "rastgele":
        sayi = random.randint(1, 100)
        await update.message.reply_text(f"Rastgele sayı: {sayi}")

    elif cmd == "tersyaz":
        if not arg_text:
            await update.message.reply_text("Bir şeyler yaz ki tersini söyleyeyim.")
        else:
            await update.message.reply_text(arg_text[::-1])

    elif cmd == "buyukharf":
        if not arg_text:
            await update.message.reply_text("Bir şeyler yaz ki büyüğe çevireyim.")
        else:
            await update.message.reply_text(arg_text.upper())

    elif cmd == "kucukharf":
        if not arg_text:
            await update.message.reply_text("Bir şeyler yaz ki küçüğe çevireyim.")
        else:
            await update.message.reply_text(arg_text.lower())

    elif cmd == "kelimesay":
        if not arg_text:
            await update.message.reply_text("Bir cümle yaz ki kelime sayayım.")
        else:
            count = len(arg_text.split())
            await update.message.reply_text(f"Kelime sayısı: {count}")

    elif cmd == "harfler":
        if not arg_text:
            await update.message.reply_text("Bir şeyler yaz ki harflerini sayayım.")
        else:
            count = len(arg_text.replace(" ", ""))
            await update.message.reply_text(f"Harfsayısı (boşluksuz): {count}")

    elif cmd == "terskelime":
        if not arg_text:
            await update.message.reply_text("Bir kelime yaz ki tersten yazayım.")
        else:
            kelimeler = arg_text.split()
            ters = " ".join(kelimeler[::-1])
            await update.message.reply_text(f"Kelime sırası ters: {ters}")

    elif cmd == "kahvefalı":
        fal = [
            "Bugün şansın açık, cesur ol!",
            "Yarın önemli bir haber alacaksın.",
            "Sevdiğin kişi yakında seni arayacak.",
            "Dikkatli ol, kıskançlık olabilir.",
            "Bir yolculuk kapıda."
        ]
        await update.message.reply_text(random.choice(fal))

    elif cmd == "doğumgünü":
        await update.message.reply_text("Doğum günün kutlu olsun! 🎉🎂")

    elif cmd == "sağlık":
        await update.message.reply_text("Bol su iç, spor yap ve sağlıklı kal!")

    elif cmd == "günaydın":
        await update.message.reply_text("Günaydın! Harika bir gün geçir!")

    elif cmd == "iyiakşamlar":
        await update.message.reply_text("İyi akşamlar! Rahatla ve dinlen!")

    elif cmd == "şifreüret":
        sifre = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=12))
        await update.message.reply_text(f"İşte sana rastgele şifre: {sifre}")

    elif cmd == "emoji":
        await update.message.reply_text("😊😂👍🔥💯🎉❤️")

    elif cmd == "kurs":
        await update.message.reply_text("Dolar: 27.5 TL\nEuro: 29.1 TL\nBitcoin: 450000 TL")

    elif cmd == "selam":
        await update.message.reply_text(f"Selam {user.first_name}! Nasılsın?")

    elif cmd == "zaman":
        now = datetime.datetime.now()
        await update.message.reply_text(f"Şu an saat: {now.strftime('%H:%M:%S')}")

    elif cmd == "tarih":
        today = datetime.date.today()
        await update.message.reply_text(f"Bugünün tarihi: {today.strftime('%d.%m.%Y')}")

    elif cmd == "fakto":
        def fakto(n):
            return 1 if n == 0 else n * fakto(n-1)
        if not arg_text or not arg_text.isdigit():
            await update.message.reply_text("Bir pozitif sayı yaz ki faktöriyelini hesaplayayım.")
        else:
            sonuc = fakto(int(arg_text))
            await update.message.reply_text(f"{arg_text}! = {sonuc}")

    elif cmd == "sondurum":
        if not arg_text:
            await update.message.reply_text("Bir ülke yaz kanka, örn: $sondurum türkiye")
        else:
            ulke = arg_text.lower()
            if ulke == "türkiye" or ulke == "turkiye":
                cevaplar = [
                    "Türkiye'nin son durumu: Herkes birbirini şaşırtmaya devam ediyor, liderimiz yine gündemde, ama biz kahvelerimizi içmeye devam! ☕😂",
                    "Türkiye siyaseti dedikodu gibi, her gün yeni bir bölüm! Liderimiz ise 'Dünya lideri' pozisyonunda, biz de ekran karşısında popcornlarımızla izliyoruz 🍿😎",
                    "Siyasi hava bugün biraz fırtınalı ama merak etme, liderimiz bir şekilde yine işleri yoluna koyacak, biz de şakalarımıza devam edeceğiz 😄",
                    "Türkiye'de siyasi durum tam bir dizi senaryosu, liderimiz başrolde, biz ise en iyi izleyicileriz!",
                ]
                await update.message.reply_text(random.choice(cevaplar))
            else:
                await update.message.reply_text(f"{arg_text.capitalize()} hakkında siyasi şaka yapamam şu an, sadece Türkiye için var bu komut 😅")

    elif cmd == "log":
        # Sadece admin kullanabilir
        if username.lower() in ADMIN_USERNAMES:
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    logs = json.load(f)
                mesajlar = ""
                for i, entry in enumerate(logs[-20:], 1):  # Son 20 mesaj
                    mesajlar += f"{i}. @{entry['user']}: {entry['message']}\n"
                if not mesajlar:
                    mesajlar = "Henüz kayıtlı mesaj yok."
                await update.message.reply_text(f"Son mesajlar:\n\n{mesajlar}")
            except Exception as e:
                await update.message.reply_text("Log dosyası okunamadı: " + str(e))
        else:
            await update.message.reply_text("Bu komutu sadece adminler kullanabilir.")

    else:
        await update.message.reply_text("Bu komutu çözemedim kanka 🤨")
