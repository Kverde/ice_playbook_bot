import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from lib.botan import Botan
from lib.setting import Setting
from source.domain import Domain


APP_ID = 'IcePlayBookBot'

setting = Setting(os.path.dirname(os.path.abspath(__file__)), APP_ID)
domain = Domain(setting)
botan = Botan(setting)

def cm_start(bot, update):
    domain.on_start(bot, update)
    botan.track(update.message, 'start')

def cm_about(bot, update):
    domain.on_about(bot, update)
    botan.track(update.message, 'about')

def cm_next(bot, update):
    domain.on_next_item(bot, update)
    botan.track(update.message, 'next')

def cm_prev(bot, update):
    domain.on_prev_item(bot, update)
    botan.track(update.message, 'prev')

def cm_random(bot, update):
    domain.on_random_item(bot, update)
    botan.track(update.message, 'random')

def cm_showMenu(bot, update):
    domain.on_menu(bot, update)
    botan.track(update.message, 'menu')

def cm_hideMenu(bot, update):
    domain.on_hide_menu(bot, update)
    botan.track(update.message, 'hidemenu')

def callb_text(bot, update):
    try:
        log_msg = domain.on_text(bot, update)
        botan.track(update.message, log_msg)
    except Exception as e:
        print(e)

def callb_error(bot, update, error):
    print('Update "%s" caused error "%s"' % (update, error))


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