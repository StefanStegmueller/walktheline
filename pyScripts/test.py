import json

with open('./settings') as json_data_file:
    data = json.load(json_data_file)
    power = data["robot"]["standard_motor_power"]
print(power)