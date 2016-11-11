from Motor import *

# This class represents a tower on a robot, that can be rotated by using a motor
class RotationTower:
    """This class represents a tower on a robot, that can be rotated by using a motor"""

    def __init__(self, port, position, robot):
        self.port = port
        self.position = position
        self.rotation_state_multiplier = 0
        self.motor = Motor(port, position)
        self.robot = robot
        self.just_rotated_back_to_origin = False

    def rotate_tower(self, direction):
        acceptable_direction = False
        movement_overloaded = False
        if direction == "left":
            power_level = 150
            acceptable_direction = True
        elif direction == "right":
            power_level = -150
            acceptable_direction = True

        maximum_tower_rotations = 2

        if (self.rotation_state_multiplier <= -maximum_tower_rotations and direction == "right") or \
                (self.rotation_state_multiplier >= maximum_tower_rotations and direction == "left"):
            acceptable_direction = False
            movement_overloaded = True


        if acceptable_direction and not movement_overloaded:
            self.motor.set_power(power_level)
            seconds = 0.2
            if power_level < 0:
                self.rotation_state_multiplier += -1
                print "Rotation state multiplier decreased to: " + str(self.rotation_state_multiplier)
            elif power_level > 0:
                self.rotation_state_multiplier += 1
                print "Rotation state multiplier increased to: " + str(self.rotation_state_multiplier)
            ot = time.time()
            while time.time() - ot < seconds:
                BrickPiUpdateValues()
                time.sleep(0.1)
            self.motor.set_power(0)
        elif movement_overloaded and not acceptable_direction:
            self.rotate_to_origin(direction)
            movement_overloaded = False

    def rotate_to_origin(self, last_movement_direction):
        self.just_rotated_back_to_origin = True
        print "ROTATE TO ORIGIN"
        power_level = 0
        if last_movement_direction == "right":
            power_level = 100
            self.robot.turn_around_z_axis(1, 175)
        elif last_movement_direction == "left":
            power_level = -100
            self.robot.turn_around_z_axis(1, -175)

        if self.rotation_state_multiplier < 0 or self.rotation_state_multiplier > 0:
            # inversion of movement history
            inverted_movement = -1*self.rotation_state_multiplier
            if last_movement_direction == "right":
                seconds = (0.1 * inverted_movement) * 1.05
            elif last_movement_direction == "left":
                seconds = (0.1 * inverted_movement) * 1.6
        else:
            inverted_movement=0
            seconds = 0
        print "Power level:" + str(power_level)
        if seconds < 0:
            seconds = -1*seconds
        print "Sekunden: " + str(seconds)
        self.motor.set_power(power_level)
        ot = time.time()
        while time.time() - ot < seconds:
            BrickPiUpdateValues()
            time.sleep(0.1)
        self.robot.turn_around_z_axis(seconds, power_level)
        self.motor.set_power(0)
        self.rotation_state_multiplier = 0

