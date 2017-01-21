import configparser
import os


class Setting():

    def __init__(self, app_path, app_id):
        self.telegram_token = self.loadSetting(app_id, 'TELEGRAM_TOKEN')
        self.botan_token = self.loadSetting(app_id, 'BOTAN_TOKEN')
        self.database_url = self.loadSetting(app_id, 'DATABASE_URL')

        self.app_path = app_path
        self.data_path = os.path.join(app_path, 'data')

    def loadSetting(self, app_id, setting_name):
        token = os.getenv(setting_name)
        if not token is None:
            return token

        setting_path = os.getenv('ice_setting')
        if setting_path is None:
            raise Exception('System var ice_setting not found')

        setting_file_name = os.path.join(setting_path, app_id, 'setting.ini')

        if not os.path.exists(setting_file_name):
            raise Exception('Setting file {} not found'.format(setting_file_name))

        config = configparser.ConfigParser()
        config.read(setting_file_name)

        res = config['main'][setting_name]

        return res.strip()


