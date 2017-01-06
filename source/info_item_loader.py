import random
import os

class InfoItem():
    def __init__(self, text, img):
        self.text = text
        self.img = img

class InfoItemLoader():
    def __init__(self, setting):
        self.setting = setting

    def loadRandomItem(self):
        n = random.randint(1, 47)
        file_name =  os.path.join(self.setting.data_path, 'item_{}.txt'.format(n))
        image_name = os.path.join(self.setting.data_path, 'img_{}.png'.format(n))

        text = ''
        for line in open(file_name, encoding='utf-8'):
            text += line

        return InfoItem(text, image_name)