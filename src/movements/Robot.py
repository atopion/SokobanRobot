#!/usr/bin/env python.
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
        self.zero_point = ColorSensor().reflected_light_intensity
        self.s = Sensors()

    def gyro_reset(self):
        """Method to reset the GyroSensor to 0"""
        self.gy.mode = 'GYRO-RATE'
        self.gy.mode = 'GYRO-ANG'

    def steer_pair_l(self):
        """Method to initalise the steering to the right side with speed set to 100"""
        self.steer_pair.on(steering=-100, speed=30)

    def steer_pair_r(self):
        """Method to initalise the steering to the left side with speed set to 100"""
        self.steer_pair.on(steering=100, speed=30)

    def steer_pair_stop(self):
        self.steer_pair.off(True)

    def turn(self, direction, count):
        """Method to calculate the right degree to turn. LEGOlas can move in the directions Up, Down, LEft, Right. Count tells LEGOlas how many squares he schould move forward in the same direction"""
        self.gyro_reset()
        i = 30
        degrees_to_turn = self.direction - direction
        #print('degrees_to_turn:', degrees_to_turn)
        if degrees_to_turn == 0:
        while i <= count:
            self.forward(self.cm_to_sec(30, 40), -1, count)
            i += 30
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
        #print(self.direction)

    def turn_right(self, count):
        """Method to turn LEGOlas 90° to the right"""
        lines_passed = 0
        i = 30
        self.gyro_reset()
        self.steer_pair_r()
        while self.gy.value() < 90:
            print("gy.value: " ,self.gy.value())
            if self.zero_point < 20:
                print("new")
                sleep(0.1)
                self.zero_point = ColorSensor().reflected_light_intensity
            if self.s.offset == self.zero_point: #Überlegen wie man reichweite von +/- 2 machen kann
                print(self.s.offset, self.zero_point)
                sleep(0.25) 
                if lines_passed == 3:
                    sleep(0.05)
                    print("Ende vong 1 Drehen her")
                    self.steer_pair_stop()
                    break
                lines_passed += 1
        while i <= count:
            self.forward(self.cm_to_sec(30, 40), -1, 30)
            i += 30 

    
    def turn_left(self, count):
        """Method to turn LEGOlas 90° to the left"""
        lines_passed = 0
        i = 30
        self.gyro_reset()
        self.steer_pair_l()
        while self.gy.value() > -100:
            print("gy.value: " ,self.gy.value())
            if self.zero_point < 20:
                print("new")
                sleep(0.1)
                self.zero_point = ColorSensor().reflected_light_intensity
            if self.s.offset == self.zero_point: #Überlegen wie man reichweite von +/- 2 machen kann
                print(self.s.offset, self.zero_point)
                sleep(0.25) 
                if lines_passed == 3:
                    sleep(0.05)
                    print("Ende vong 1 Drehen her")
                    self.steer_pair_stop()
                    break
                lines_passed += 1
        while i <= count:
            self.forward(self.cm_to_sec(30, 40), 1, 30)
            i += 30
    
    def turn_back(self, count):
        """Method to turn LEGOlas 180° around"""
        lines_passed = 0
        i = 30
        self.gyro_reset()
        self.steer_pair_r()
        while self.gy.value() < 200:
            if self.zero_point < 20:
                print("new")
                sleep(0.1)
                self.zero_point = ColorSensor().reflected_light_intensity
            if self.s.offset == self.zero_point: #Überlegen wie man reichweite von +/- 2 machen kann
                sleep(0.25) 
                if lines_passed == 3:
                    print("Ende vong 1 Drehen her")
                    sleep(0.05)
                    self.steer_pair_stop()
                    break
                lines_passed += 1
        while i <= count:
            self.forward(self.cm_to_sec(30, 40), 1, 30)
            i += 30

    def forward(self, x, y, count):
        """Method for driving the robot x seconds forward until LEGOlas reached a crossing"""
        self.s.pid(x, y, count)
        sleep(1)
            
    def cm_to_sec(self, cm, speed):
        """Function to calculate how many seconds the roboter have to move with speed x to drive n cm"""
        sec = 0.0   
        ref_sec = 2.9
        ref_cm = 1
        ref_speed = 1
        sec = ref_sec * cm / speed
        print('sec: ', sec)
        return sec




