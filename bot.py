from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from main import (
    start,
    about,
    contact,
    contact_callback,
    buy,
)
import os


TOKEN = os.environ.get("TOKEN")

def main():
    # updater
    updater = Updater(token=TOKEN)
    # dispatcher
    dispatcher = updater.dispatcher
    # handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text('📝 About'), about))
    dispatcher.add_handler(MessageHandler(Filters.text('📞 Contact'), contact))
    dispatcher.add_handler(MessageHandler(Filters.text('🛒 Buy'), buy))
    dispatcher.add_handler(CallbackQueryHandler(contact_callback))

    # start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()