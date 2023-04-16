from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)
from telegram.ext import (
    CallbackContext,
)
from db import UserDb, ProductDB
from tinydb import TinyDB,Query
sanoqdb = TinyDB('sanoq.json', indent=4)
userdb = UserDb()
User=Query()
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
    # inline keyboard
    inline_keyboard = [
        [   
            InlineKeyboardButton('📞Phone', callback_data='1.phone-number'), 
            InlineKeyboardButton('📧Email', callback_data='1.email-address')
        ],
        [
            InlineKeyboardButton('📍Location', callback_data='1.location'),
            InlineKeyboardButton('🎯Address', callback_data='1.address')
        ]
    ]

    # send message
    update.message.reply_text('Contact us:', reply_markup=InlineKeyboardMarkup(inline_keyboard))


def contact_callback(update: Update, context):
    '''Contact callback handler'''
    # get callback data
    query = update.callback_query
    data = query.data.split('.')[-1]
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
def products(update: Update, context):
    query=update.callback_query
    brands1=update.callback_query.data.split(":")[-1]
    products=productdb.get_product_by_brand(brand=brands1)
    inline_keyboard = []
    product_id=0
    for product in products:
        brand=product['name']
        company=product['company']
        product_id+=1
        inline_keyboard.append([InlineKeyboardButton(text=brand, callback_data=f'product:{brand}:{company}:{product_id}')])
    inline_keyboard.append([InlineKeyboardButton('❌ Close', callback_data='close')])
    # send message
    query.edit_message_text(text='All products:', reply_markup=InlineKeyboardMarkup(inline_keyboard))   
def close(update: Update, context):
    query=update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)
    query.answer('Closed')
def product(update: Update, context):
    query=update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    brands1=update.callback_query.data.split(":")[2]
    product_id=update.callback_query.data.split(":")[-1]
    sanoqdb.insert({'chat_id':chat_id,'sanoq':product_id})
    product=productdb.get_product(brand=brands1,product_id=product_id)
    price = product['price']
    ram = product['RAM']
    memory = product['memory']
    name = product['name']
    color = product['color']
    img = product['img_url']
    text=f"📲{name}\n\n🎨{color}\n💾{ram}/{memory}\n💰{price}\n\n@telefonBozor"
    button1 = InlineKeyboardButton('<--',callback_data=f'dddorqaga_{brands1}_{product_id}_last')
    button2 = InlineKeyboardButton('Add',callback_data=f'saqlash_{brands1}')
    button3 = InlineKeyboardButton('-->',callback_data=f'dddoldinga_{brands1}_{product_id}_next')
    button4 = InlineKeyboardButton('❌ Close',callback_data='uchir')
    inline_keybord=InlineKeyboardMarkup([[button1, button2,button3],[button4]])
    bot.send_photo(chat_id=query.message.chat.id, photo=img, caption=text, reply_markup=inline_keybord)
def oldinga_orqaga(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    data = query.data.split('_')[-1]
    #product_id=update.callback_query.data.split("_")[2]
    k=int(sanoqdb.get(User.chat_id==chat_id)['sanoq'])
    print(k)
    brands1=update.callback_query.data.split("_")[1]
    products=productdb.get_product_by_brand(brand=brands1)
    max1=len(products)
    if k==max1:
        sanoqdb.update({'sanoq':0}, User.chat_id==chat_id)
    if k==1:
        sanoqdb.update({'sanoq':max1}, User.chat_id==chat_id)
    print(max1)
    if data=="last":
        k-=1

        product=productdb.get_product(brand=brands1,product_id=k)
        price = product['price']
        ram = product['RAM']
        memory = product['memory']
        name = product['name']
        color = product['color']
        img = product['img_url']
        text=f"📲{name}\n\n🎨{color}\n💾{ram}/{memory}\n💰{price}\n\n@telefonBozor"
        button1 = InlineKeyboardButton('<--',callback_data=f'dddorqaga_{brands1}_last')
        button2 = InlineKeyboardButton('Add',callback_data=f'saqlash_{brands1}')
        button3 = InlineKeyboardButton('-->',callback_data=f'dddoldinga_{brands1}_next')
        button4 = InlineKeyboardButton('❌ Close',callback_data='uchir')
        inline_keybord=InlineKeyboardMarkup([[button1, button2,button3],[button4]])
        query.edit_message_media(media=InputMediaPhoto(media=img, caption=text), reply_markup=inline_keybord)
        sanoqdb.update({'sanoq':k}, User.chat_id==chat_id)
    if data=="next":   
        k+=1

        product=productdb.get_product(brand=brands1,product_id=k)
        price = product['price']
        ram = product['RAM']
        memory = product['memory']
        name = product['name']
        color = product['color']
        img = product['img_url']
        text=f"📲{name}\n\n🎨{color}\n💾{ram}/{memory}\n💰{price}\n\n@telefonBozor"
        button1 = InlineKeyboardButton('<--',callback_data=f'dddorqaga_{brands1}_last')
        button2 = InlineKeyboardButton('Add',callback_data=f'saqlash_{brands1}')
        button3 = InlineKeyboardButton('-->',callback_data=f'dddoldinga_{brands1}_next')
        button4 = InlineKeyboardButton('❌ Close',callback_data='uchir')
        inline_keybord=InlineKeyboardMarkup([[button1, button2,button3],[button4]])
        query.edit_message_media(media=InputMediaPhoto(media=img, caption=text), reply_markup=inline_keybord)
        sanoqdb.update({'sanoq':k}, User.chat_id==chat_id)
def adds(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    brands= query.data.split('_')[-1]
    k=int(sanoqdb.get(User.chat_id==chat_id)['sanoq'])
    userdb.add_order(chat_id=chat_id, product_id=k,company=brands)
    query.answer("Qo`shildi✅")
def order(update: Update, context):
    text='Mening xaridlarim:'
    button1 = InlineKeyboardButton(' 📦 Cart',callback_data='olindi')
    button2 = InlineKeyboardButton('📝 Clear cart',callback_data='clear')
    button3 = InlineKeyboardButton('❌ Close',callback_data='uchir')
    inline_keybord=InlineKeyboardMarkup([[button1, button2,button3]])
    update.message.reply_text(text=text, reply_markup=inline_keybord)
def orders(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    print(chat_id)
    orders = userdb.get_order(chat_id=chat_id)
    print(orders)
    if orders==[]:
        text="Savat bo`sh."
    else:
        text=""
        i=1
        for order in orders:
            company=order['company']
            product_id=order['product_id']
            product=productdb.get_product(brand=company,product_id=product_id)
            name = product['name']
            price = product['price']
            text+=f'{i} 📲 {name} \n💰{price}\n\n '
            i+=1

    button1 = InlineKeyboardButton(' 📦 Maxsulotlarni olish',callback_data='yuborildi')
    inline_keybord=InlineKeyboardMarkup([[button1]])
    query.edit_message_text(text=text, reply_markup=inline_keybord)
def bildirish(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    query.answer("Buyurtmalaringiz Yuborildi ✅")
def clear(update: Update, context: CallbackContext):
    '''handle clear button'''
    query = update.callback_query
    data = query.data

    userdb.clear_order(query.from_user.id)
    query.answer('Cleared')


