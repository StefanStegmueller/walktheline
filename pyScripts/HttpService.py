import requests
import json

class HttpService:

    def __init__(self):
        self.json_data = None
        self.direction = None
        self.wait_for_manual_instruction = None

    def set_data(self, roi_position, roi_height, path_position, on_track, wait_for_manual_instruction):
        self.json_data = {
            "roi_position": roi_position,
            "roi_height": roi_height,
            "path_position": path_position,
            "path_width": 0,
            "on_track": on_track,
            "wait_for_manual_instruction": wait_for_manual_instruction
        }

    def send_data(self, url, file):
        files = {'file': open(file)}
        response = requests.post(url, files=files, data=self.json_data)
        print response.text
        data = response.json()
	#print data
        self.direction = data['direction']
        self.wait_for_manual_instruction = data['wait_for_manual_instruction']
