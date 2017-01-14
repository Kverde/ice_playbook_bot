import random
import os

class InfoItem():
    def __init__(self, text, img):
        self.text = text
        self.img = img

class InfoItemLoader():
    def __init__(self, setting):
        self.setting = setting

    def loadItem(self, item_index):

        file_name =  os.path.join(self.setting.data_path, 'item_{}.txt'.format(item_index))
        image_name = os.path.join(self.setting.data_path, 'img_{}.png'.format(item_index))

        text = ''
        for line in open(file_name, encoding='utf-8'):
            text += line

        return InfoItem(text, image_name)

    def loadRandomItem(self):
        n = random.randint(1, 47)
        return self.loadItem(n)