import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import handle_command

# Loglama ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

import config  # config.py içinde BOT_TOKEN var

async def on_message(update, context):
    await handle_command(update, context)

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Mesajları yakala
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), on_message))
    # Komutlar $ işaretli olduğu için filtrelemek zor değil,
    # tüm metin mesajları handle_command tarafından işleniyor.

    # $start gibi komutlar da handle_command içinde kontrol ediliyor.

    print("Bot çalışıyor...")

    app.run_polling()

if __name__ == "__main__":
    main()
