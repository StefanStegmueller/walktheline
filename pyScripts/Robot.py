from BrickPi import *  # import BrickPi.py file to use BrickPi operations

# This class is an abstract representation of a Robot, consisting of sensors and actors
class Robot:
    """This class is an abstract representation of a Robot, consisting of sensors and actors"""

    def __init__(self):
        self.motors = []
        self.sensors = []

    def set_motors(self, motor_list):
        self.motors = motor_list

    def set_sensors(self, sensor_list):
        self.sensors = sensor_list

    def set_motor_power(self, position, motor_power_level):
        for each_motor in self.motors:
            if each_motor.position == position:
                each_motor.set_power(motor_power_level)

    def get_motor_power(self, position):
        for each_motor in self.motors:
            if each_motor.position == position:
                each_motor.get_power()

    def set_both_motor_powers(self, motor_power_level):
        for each_motor in self.motors:
            BrickPi.MotorSpeed[each_motor.port] = motor_power_level

    def drive_backwards(self, seconds, motor_power_level):
        """Let the robot drive backwards for a given amount of seconds"""
        if motor_power_level > 0:
            motor_power_level = -motor_power_level
        self.set_both_motor_powers(motor_power_level)

        start_time = time.time()
        while time.time() - start_time < seconds:
            BrickPiUpdateValues()
            time.sleep(0.1)

    def drive_forward(self, seconds, motor_power_level):
        """Let the robot drive forward for a given amount of seconds"""
        if motor_power_level < 0:
            motor_power_level = -motor_power_level
        self.set_both_motor_powers(motor_power_level)

        ot = time.time()
        while time.time() - ot < seconds:
            BrickPiUpdateValues()
            time.sleep(0.1)

    def handbrake(self):
        """Stops the engines hard"""
        self.set_both_motor_powers(0)
        BrickPiUpdateValues()
        time.sleep(0.1)

    def turn_around_z_axis(self, seconds, motor_power_value):
        """Let the robot turn around the Z axis"""
        # if motor_power is negative, the robot turns to the right and if it's positive, it turns to the left
        self.set_motor_power("left", -motor_power_value)
        self.set_motor_power("right", motor_power_value)

        start_time = time.time()
        while time.time() - start_time < seconds:
            BrickPiUpdateValues()
            time.sleep(0.1)

    def correct_deviation(self, deviation, standart_power):
        tolerance = 20
        correction_factor = 1
        if(deviation > 0 + tolerance ):
            curve_power = abs(deviation) * correction_factor
            self.set_motor_power("right",curve_power)
            self.set_motor_power("left", standart_power - curve_power)
        elif(deviation < 0 - tolerance):
            curve_power = abs(deviation) * correction_factor
            self.set_motor_power("left", curve_power)
            self.set_motor_power("right", standart_power - curve_power)
        else:
            self.set_both_motor_powers(standart_power)

