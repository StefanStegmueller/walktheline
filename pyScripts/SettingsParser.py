import json

class SettingsParser:

    @staticmethod
    def get_value(object_name, attribute_name):
        data = SettingsParser.read_settings()
        return data[object_name][attribute_name]

    @staticmethod
    def read_settings():
        with open('settings') as json_data_file:
            data = json.load(json_data_file)
        return data