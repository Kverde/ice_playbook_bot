from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram

import source.db
from source.setting import Setting
from source.info_item_loader import InfoItemLoader

APP_ID = 'IcePlayBookBot'

setting = Setting(APP_ID)
itemLoader = InfoItemLoader(setting)

BUTTON_PREV = 0
BUTTON_NEXT = 1
BUTTON_RANDOM = 2
BUTTON_ABOUT = 3

BUTTON_CAPTIONS = {
    BUTTON_PREV: 'Предыдущая запись',
    BUTTON_NEXT: 'Следующая запись',
    BUTTON_RANDOM: 'Случайная запись',
    BUTTON_ABOUT: 'Спиок источников',
}

about_text = '''
  Записи берутся из разных источников, список:

  <a href="https://techcrunch.com/2010/08/25/scvngr-game-mechanics/">SCVNGR game mechanics</a>

  Если здесь не упомянут какой-то из источников записей, пожалуйста, свяжитесь с @Kverde
'''

def sendAbout(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=about_text,
                    parse_mode=telegram.ParseMode.HTML)

def sendItem(bot, update, item_index):
    try:
        item = itemLoader.loadItem(item_index)

        bot.sendPhoto(chat_id=update.message.chat_id,
                      photo=open(item.img, 'rb'))

        bot.sendMessage(chat_id=update.message.chat_id,
                        text=item.text,
                        parse_mode=telegram.ParseMode.HTML)
    except Exception as e:
        print(e)

def sendRandomItem(bot, update):
    try:
        item = itemLoader.loadRandomItem()

        bot.sendPhoto(chat_id=update.message.chat_id,
                      photo=open(item.img, 'rb'))

        bot.sendMessage(chat_id=update.message.chat_id,
                        text=item.text,
                        parse_mode=telegram.ParseMode.HTML)
    except Exception as e:
        print(e)

def sendMenu(bot, update):
    keyboard = [[KeyboardButton(BUTTON_CAPTIONS[BUTTON_PREV], callback_data=BUTTON_PREV),
                 KeyboardButton(BUTTON_CAPTIONS[BUTTON_NEXT], callback_data=BUTTON_NEXT)],

                [KeyboardButton(BUTTON_CAPTIONS[BUTTON_RANDOM], callback_data=BUTTON_RANDOM)],
                [KeyboardButton(BUTTON_CAPTIONS[BUTTON_ABOUT], callback_data=BUTTON_ABOUT)]]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Для навигации используйте меню:', reply_markup=reply_markup)

def sendHideMenu(bot, update):
    reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Скрыть клавиатуру",
                    reply_markup=reply_markup)

def sendNextItem(bot, update):
    print('next_item')
    try:
        sendItem(bot, update, source.db.getNext(update.message.from_user.id))
    except Exception as e:
        print(e)

def sendPrevItem(bot, update):
    print('prev_item')
    try:
        sendItem(bot, update, source.db.getPrev(update.message.from_user.id))
    except Exception as e:
        print(e)


def cm_start(bot, update):
    update.message.reply_text('Для навигации используйте меню или команды.')

    sendMenu(bot, update)

MENU_EVENTS = {
    BUTTON_CAPTIONS[BUTTON_PREV]: sendPrevItem,
    BUTTON_CAPTIONS[BUTTON_NEXT]: sendNextItem,
    BUTTON_CAPTIONS[BUTTON_RANDOM]: sendRandomItem,
    BUTTON_CAPTIONS[BUTTON_ABOUT]: sendAbout,
}

def callb_error(bot, update, error):
    print('Update "%s" caused error "%s"' % (update, error))

def cm_about(bot, update):
    sendAbout(bot, update)

def cm_next(bot, update):
    sendNextItem(bot, update)

def cm_prev(bot, update):
    sendPrevItem(bot, update)

def cm_random(bot, update):
    sendRandomItem(bot, update)

def cm_showMenu(bot, update):
    sendMenu(bot, update)

def cm_hideMenu(bot, update):
    sendHideMenu(bot, update)

def callb_text(bot, update):
    if update.message.text in MENU_EVENTS:
        MENU_EVENTS[update.message.text](bot, update)
    else:
        print('text')
        sendRandomItem(bot, update)
        user = update.message.from_user
        print(user)
        print('{} - {} - {} - {}'.format(user.id))

updater = Updater(setting.telegram_token)

updater.dispatcher.add_handler(CommandHandler('start', cm_start))
updater.dispatcher.add_handler(CommandHandler('about', cm_about))
updater.dispatcher.add_handler(CommandHandler('next', cm_next))
updater.dispatcher.add_handler(CommandHandler('prev', cm_prev))
updater.dispatcher.add_handler(CommandHandler('showmenu', cm_showMenu))
updater.dispatcher.add_handler(CommandHandler('hidemenu', cm_hideMenu))

updater.dispatcher.add_handler(MessageHandler(Filters.text, callb_text))

updater.dispatcher.add_error_handler(callb_error)

updater.start_polling()
updater.idle()