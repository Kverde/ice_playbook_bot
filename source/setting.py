import configparser
import os



class Setting():
    def __init__(self, app_id):
        self.telegram_token = self.loadTelegramToken(app_id)
        self.data_path = r'data\\'

    def loadTelegramToken(self, app_id):
        token = os.getenv('TELEGRAM_TOKEN')
        if not token is None:
            return token

        setting_path = os.getenv('ice_setting')
        if setting_path is None:
            raise Exception('System var ice_setting not found')

        settingFileName = os.path.join(setting_path, app_id, 'setting.ini')

        if not os.path.exists(settingFileName):
            raise Exception('Setting file {} not found'.format(settingFileName))

        config = configparser.ConfigParser()
        config.read(settingFileName)

        return config['main']['telegram_token']
