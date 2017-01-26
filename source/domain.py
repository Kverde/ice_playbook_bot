from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
import os

from source.db import Db
from source.info_item_loader import InfoItemLoader

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
Пожалуйста, оцените этого бота https://telegram.me/storebot?start=IcePlaybookBot

Список статей, и авторов:

<a href="https://techcrunch.com/2010/08/25/scvngr-game-mechanics/">SCVNGR game mechanics</a>

Если упомянуты не все, пожалуйста, сообщите об этом.

Для связи с разработчиком используйте Telegram @KonstantinShpilko, сайт http://way23.ru
'''

class Domain():

    def __init__(self, setting):
        self.MENU_EVENTS = {
            BUTTON_CAPTIONS[BUTTON_PREV]: self.on_prev_item,
            BUTTON_CAPTIONS[BUTTON_NEXT]: self.on_next_item,
            BUTTON_CAPTIONS[BUTTON_RANDOM]: self.on_random_item,
            BUTTON_CAPTIONS[BUTTON_ABOUT]: self.on_about,
        }

        self.item_loader = InfoItemLoader(setting)

        self.db = Db(setting)

    def on_start(self, bot, update):
        update.message.reply_text('Привет!')
        self.on_menu(bot, update)

    def on_about(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=about_text,
                        parse_mode=telegram.ParseMode.HTML)
        return 'about'

    def on_random_item(self, bot, update):
        item = self.item_loader.loadRandomItem()
        self.send_tem(bot, update, item)
        return 'random'


    def on_menu(self, bot, update):
        keyboard = [[KeyboardButton(BUTTON_CAPTIONS[BUTTON_PREV], callback_data=BUTTON_PREV),
                     KeyboardButton(BUTTON_CAPTIONS[BUTTON_NEXT], callback_data=BUTTON_NEXT)],

                    [KeyboardButton(BUTTON_CAPTIONS[BUTTON_RANDOM], callback_data=BUTTON_RANDOM)],
                    [KeyboardButton(BUTTON_CAPTIONS[BUTTON_ABOUT], callback_data=BUTTON_ABOUT)]]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        update.message.reply_text('Для навигации используйте меню', reply_markup=reply_markup)

    def on_hide_menu(self, bot, update):
        reply_markup = telegram.ReplyKeyboardHide()
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Скрыть клавиатуру",
                        reply_markup=reply_markup)

    def on_next_item(self, bot, update):
        self.send_item_index(bot, update, self.db.getNext(update.message.from_user.id))
        return 'next'

    def on_prev_item(self, bot, update):
        self.send_item_index(bot, update, self.db.getPrev(update.message.from_user.id))
        return 'prev'

    def on_text(self, bot, update):
        if update.message.text in self.MENU_EVENTS:
            return self.MENU_EVENTS[update.message.text](bot, update)
        else:
            self.on_random_item(bot, update)
            return 'text'


    def send_tem(self, bot, update, item):

        if os.path.isfile(item.img):
            bot.sendPhoto(chat_id=update.message.chat_id,
                          photo=open(item.img, 'rb'))

        bot.sendMessage(chat_id=update.message.chat_id,
                        text=item.text,
                        parse_mode=telegram.ParseMode.HTML)

    def send_item_index(self, bot, update, item_index):
        item = self.item_loader.loadItem(item_index)
        self.send_tem(bot, update, item)
