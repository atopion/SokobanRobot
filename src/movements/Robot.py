#!/usr/bin/env python3
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_D, LargeMotor, MoveSteering
from ev3dev2.sensor.lego import GyroSensor
from time import sleep
from Directions import  Directions
from Sensors import Sensors
from ev3dev2.sensor.lego import ColorSensor    

class Robot():
#"""Class for roboter movements."""

    def __init__(self):
        """Constructor for the internal state of the robot, e.g. in which direction he is
        currently looking"""
        self.direction = Directions.up
        self.gy = GyroSensor()
        self.steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class= LargeMotor)
        self.zero_point = ColorSensor.reflected_light_intensity
        self.s = Sensors()

    def gyro_reset(self):
        """Method to reset the GyroSensor to 0"""
        self.gy.mode = 'GYRO-RATE'
        self.gy.mode = 'GYRO-ANG'

    def steer_pair_l(self):
        """Method to initalise the steering to the right side with speed set to 100"""
        self.steer_pair.on(steering=-100, speed=50)

    def steer_pair_r(self):
        """Method to initalise the steering to the left side with speed set to 100"""
        self.steer_pair.on(steering=100, speed=50)

    def steer_pair_stop(self):
        self.steer_pair.off(True)

    def turn(self, direction, count):
        """Method to calculate the right degree to turn. LEGOlas can move in the directions Up, Down, LEft, Right. Count tells LEGOlas how many squares he schould move forward in the same direction"""
        self.gyro_reset()
        degrees_to_turn = self.direction - direction
        print('degrees_to_turn:', degrees_to_turn)
        if degrees_to_turn == 0:
            self.forward(self.cm_to_sec(count, 26))
            return 
        switcher = {
                -3: self.turn_left,  #reference to method turn_x (in this "switch" only references are allowed)
                -2: self.turn_back,
                -1: self.turn_right,
                1: self.turn_left,
                2: self.turn_back,
                3: self.turn_right,
        }
        func = switcher.get(degrees_to_turn, "Invalid direction")
        func(count)
        self.direction = direction
        print(self.direction)

    def turn_right(self, count):
        """Method to turn LEGOlas 90° to the right"""
        self.gyro_reset()
        self.steer_pair_r()
        while self.gy.value() < 100:
            if self.s.offset == self.zero_point: #Überlegen wie man reichweite von +/- 2 machen kann
                self.steer_pair_stop()
                break
        self.forward(self.cm_to_sec(count, 20))
    
    def turn_left(self, count):
        """Method to turn LEGOlas 90° to the left"""
        lines_passed = False
        self.gyro_reset()
        self.steer_pair_l()
        while self.gy.value() > -96:
            print(self.gy.value())
            if self.s.offset == self.zero_point:
                if lines_passed == True:
                    self.steer_pair_stop()
                    break
                lines_passed = True
        self.forward(self.cm_to_sec(count, 20))
    
    def turn_back(self, count):
        """Method to turn LEGOlas 180° around"""
        self.gyro_reset()
        lines_passed = 0
        self.steer_pair_r()
        while self.gy.value() < 200:
            if self.s.offset == self.zero_point:
                if lines_passed == 2:
                    self.steer_pair_stop()
                    break
                lines_passed += 1
        self.forward(self.cm_to_sec(count, 20))

    def forward(self, x):
        """Method for driving the robot x seconds forward"""
        self.s.pid(x)
        sleep(1)
            
    def cm_to_sec(self, cm, speed):
        """Function to calculate how many seconds the roboter have to move with speed x to drive n cm"""
        sec = 0.0   
        ref_sec = 3.85
        ref_cm = 1
        ref_speed = 1
        sec = ref_sec * cm / speed
        print('sec:', sec)
        return sec




