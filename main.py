from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from db import UserDb, ProductDB

userdb = UserDb()
productdb = ProductDB()

def start(update: Update, context):
    '''Start command handler'''
    # get user info
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    # add user to db
    result = userdb.add_user(chat_id, first_name, username, last_name)
    # menu buttons
    keyboard = [
        [KeyboardButton('🛒 Buy'), KeyboardButton('📦 Order')],
        [KeyboardButton('📝 About'), KeyboardButton('📞 Contact')],
    ]
    # send message
    if result:
        update.message.reply_text(f'Hi {first_name}! Welcome to our bot!', reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    else:
        update.message.reply_text(f'Hi {first_name}! Welcome back!', reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


def about(update: Update, context):
    '''About command handler'''
    # send message
    update.message.reply_text('This is a bot for buying products from different companies.')


def contact(update: Update, context):
    '''Contact command handler'''
    query=update.callback_query
    data=query.data
    inline_keyboard = [
        
        [InlineKeyboardButton('📞 Phone number'), InlineKeyboardButton('📌 Address')],
        [InlineKeyboardButton('📍 Location'), InlineKeyboardButton('📧 Email')],]
    query.edit_message_text('Contact menu', reply_markup=InlineKeyboardMarkup(inline_keyboard))
    # inline keyboard
    inline_keyboard = [
        [   
            InlineKeyboardButton('📞Phone', callback_data='phone-number'), 
            InlineKeyboardButton('📧Email', callback_data='email-address')
        ],
        [
            InlineKeyboardButton('📍Location', callback_data='location'),
            InlineKeyboardButton('🎯Address', callback_data='address')
        ]
    ]

    # send message
    update.message.reply_text('Contact us:', reply_markup=InlineKeyboardMarkup(inline_keyboard))


def contact_callback(update: Update, context):
    '''Contact callback handler'''
    # get callback data
    query = update.callback_query
    data = query.data
    # send message
    if data == 'phone-number':
        query.edit_message_text(text='Phone number: 998 90 123 45 67')
    elif data == 'email-address':
        query.edit_message_text(text='Email: example@gmail.com')
    elif data == 'location':
        query.delete_message()
        context.bot.send_location(chat_id=query.message.chat_id, latitude=41.311081, longitude=69.240562)
    elif data == 'address':
        query.edit_message_text(text='Address: Tashkent, Uzbekistan')


def buy(update: Update, context):
    '''Buy command handler'''
    # get all brands from db
    brands = productdb.get_brand()
    # menu inline menu
    inline_keyboard = []
    for brand in brands:
        inline_keyboard.append([InlineKeyboardButton(text=brand, callback_data=f'brand:{brand}')])
    
    # close button
    inline_keyboard.append([InlineKeyboardButton('❌ Close', callback_data='close')])
    # send message
    update.message.reply_text('Choose a brand:', reply_markup=InlineKeyboardMarkup(inline_keyboard))

