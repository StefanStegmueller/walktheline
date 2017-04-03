from BrickPi import *    # import BrickPi.py file to use BrickPi operations


# This class is an abstract representation of a motor engine
class Motor:
    """This class is an abstract representation of a motor engine"""

    def __init__(self, port, position):
        self.__port = port
        self.__position = position

    def get_position(self):
        return self.__position

    def get_port(self):
        return self.__port

    def set_power(self, level):
        BrickPi.MotorSpeed[self.__port] = level

    def get_power(self):
        return BrickPi.MotorSpeed[self.__port]
