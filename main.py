import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

from source.setting import Setting
from source.info_item_loader import InfoItemLoader

APP_ID = 'IcePlayBookBot'

setting = Setting(APP_ID)
itemLoader = InfoItemLoader(setting)

def start(bot, update):
    update.message.reply_text('В ответ на любое сообщение вы получите случайную запись!')
    update.message.reply_text(r'Список источников вы может получить командой /about')

about_text = '''
  Записи берутся из разных источников, список:

  <a href="https://techcrunch.com/2010/08/25/scvngr-game-mechanics/">SCVNGR game mechanics</a>

  Если здесь не упомянут какой-то из источников записей, пожалуйста, свяжитесь с @Kverde
'''

def about(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=about_text,
                    parse_mode=telegram.ParseMode.HTML)

def text(bot, update):
    try:
        item = itemLoader.loadRandomItem()

        bot.sendPhoto(chat_id=update.message.chat_id,
                      photo=open(item.img, 'rb'))

        bot.sendMessage(chat_id=update.message.chat_id,
                        text=item.text,
                        parse_mode=telegram.ParseMode.HTML)
    except Exception as e:
        print(e)

updater = Updater(setting.telegram_token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(MessageHandler(Filters.text, text))

updater.start_polling()
updater.idle()