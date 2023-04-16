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
    products,
    close,
    product,
    oldinga_orqaga,
    order,
    bildirish,
    adds,
    orders,
    clear,
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
    dispatcher.add_handler(MessageHandler(Filters.text('📦 Order'), order))
    dispatcher.add_handler(CallbackQueryHandler(contact_callback, pattern="1"))
    dispatcher.add_handler(CallbackQueryHandler(products, pattern="brand"))
    dispatcher.add_handler(CallbackQueryHandler(close, pattern="close"))
    dispatcher.add_handler(CallbackQueryHandler(close, pattern="uchir"))
    dispatcher.add_handler(CallbackQueryHandler(product, pattern="product"))
    dispatcher.add_handler(CallbackQueryHandler(oldinga_orqaga, pattern="ddd"))
    dispatcher.add_handler(CallbackQueryHandler(bildirish, pattern="yuborildi"))
    dispatcher.add_handler(CallbackQueryHandler(adds, pattern="saqlash"))
    dispatcher.add_handler(CallbackQueryHandler(orders, pattern="olindi"))
    dispatcher.add_handler(CallbackQueryHandler(clear, pattern="clear"))







    # start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()