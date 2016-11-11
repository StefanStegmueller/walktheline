from BrickPi import *    # import BrickPi.py file to use BrickPi operations


# This class is an abstract representation of a motor engine
class Motor:
    """This class is an abstract representation of a motor engine"""

    def __init__(self, port, position):
        self.port = port
        self.position = position

    def set_power(self, level):
        BrickPi.MotorSpeed[self.port] = level

    def get_power(self):
        return BrickPi.MotorSpeed[self.port]
