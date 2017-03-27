import requests
import json

class HttpService:

    def __init__(self):
        self.__json_data = None
        self.__manual_direction = None

    def get_manual_direction(self):
        return self.__manual_direction

    def set_data(self, roi_position, roi_height, path_position):
        self.__json_data = {
            "roi_position": roi_position,
            "roi_height": roi_height,
            "path_position": path_position,
            "path_width": 0
        }

    def send_data(self, url, file):
        files = {'file': open(file)}
        response = requests.post(url, files=files, data=self.__json_data)
        print response.text
        data = response.json()

        self.__manual_direction = data['direction']
