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
        self.quit = 0
        self.side_to_follow = 1

    def new_zero_point(self):
        self.zero_point = 25
        print("Künstlicher Nullpunkt")

    def gyro_reset(self):
        """Method to reset the GyroSensor to 0"""
        self.gy.mode = 'GYRO-RATE'
        self.gy.mode = 'GYRO-ANG'

    def steer_pair_l(self):
        """Method to initalise the steering to the right side with speed set to 100"""
        self.steer_pair.on(steering=-100, speed=25)

    def steer_pair_r(self):
        """Method to initalise the steering to the left side with speed set to 100"""
        self.steer_pair.on(steering=100, speed=25)

    def steer_pair_stop(self):
        self.steer_pair.off(True)

    def turn(self, direction, count, opposite): 
        """Method to calculate the right degree to turn. LEGOlas can move in the directions Up, Down, LEft, Right. Count tells LEGOlas how many squares he schould move forward in the same direction"""
        self.gyro_reset()
        if self.zero_point < 25:
            self.new_zero_point()
        i = 30
        degrees_to_turn = self.direction - direction
        if degrees_to_turn == 0:
            while i <= count:
                self.quit = self.forward(self.cm_to_sec(30, 40), -1, 30, opposite)
                self.side_to_follow = -1
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
        func(count, degrees_to_turn, opposite)
        self.direction = direction
        #print(self.direction)

    def turn_right(self, count, degrees_to_turn, opposite):
        """Method to turn LEGOlas 90° to the right"""
        lines_passed = 0
        i = 30
        self.gyro_reset()
        self.steer_pair_r()
        while self.gy.value() < 90:
            print("gy.value: " ,self.gy.value(), "reflected_light_intensity: ", ColorSensor().reflected_light_intensity)
            if ColorSensor().reflected_light_intensity <= 22 and self.gy.value() > 45: #Überlegen wie man reichweite von +/- 2 machen kann
                print(self.s.offset, ColorSensor().reflected_light_intensity)
                sleep(0.16)
                self.steer_pair_stop()
                break
        while i <= count:
            print("opposite: ", opposite)
            self.quit = self.forward(self.cm_to_sec(30, 40), -1, 30, opposite)
            self.side_to_follow = -1
            i += 30 

    
    def turn_left(self, count, degrees_to_turn, opposite):
        """Method to turn LEGOlas 90° to the left"""
        lines_passed = 0
        i = 30
        self.gyro_reset()
        self.steer_pair_l()
        while self.gy.value() > -90:
            print("gy.value: " ,self.gy.value(), "reflected_light_intensity: ", ColorSensor().reflected_light_intensity)
            if ColorSensor().reflected_light_intensity <= 22 and self.gy.value() < -45: #Überlegen wie man reichweite von +/- 2 machen kann
                print(self.s.offset, ColorSensor().reflected_light_intensity)
                sleep(0.16) 
                self.steer_pair_stop()
                break   
        while i <= count:
            print("opposite: ", opposite)
            self.quit = self.forward(self.cm_to_sec(30, 40), 1, 30, opposite)
            self.side_to_follow = 1
            i += 30
    
    def turn_back(self, count, degrees_to_turn, opposite):
        """Method to turn LEGOlas 180° around"""
        self.gyro_reset()
        lines_passed = 0
        i = 30
        if degrees_to_turn == -2:
            self.steer_pair_r()
            while self.gy.value() < 178:
                print("gy.value: " ,self.gy.value(), "reflected_light_intensity: ", ColorSensor().reflected_light_intensity)
                if ColorSensor().reflected_light_intensity <= 22 and self.gy.value() > 140: #Überlegen wie man reichweite von +/- 2 machen kann
                    print(self.s.offset, ColorSensor().reflected_light_intensity)
                    sleep(0.14)
                    self.steer_pair_stop()
                    break
            if self.side_to_follow == -1:
                while i <= count:
                    if self.quit == 1:
                        self.quit = self.forward(self.cm_to_sec(20, 40), 1, 30, opposite)
                        self.side_to_follow = 1
                        i += 30
                    else:
                        self.quit = self.forward(self.cm_to_sec(30, 40), 1, 30, opposite)
                        self.side_to_follow = 1
                        i += 30
            else: 
                while i <= count:
                    if self.quit == 1:
                        self.quit = self.forward(self.cm_to_sec(20, 40), -1, 30, opposite)
                        self.side_to_follow = -1
                        i += 30
                    else:
                        self.quit = self.forward(self.cm_to_sec(30, 40), -1, 30, opposite)
                        self.side_to_follow = -1
                        i += 30
        else:
            self.steer_pair_l()
            while self.gy.value() > -178:
                print("gy.value: " ,self.gy.value(), "reflected_light_intensity: ", ColorSensor().reflected_light_intensity)
                if ColorSensor().reflected_light_intensity <= 22 and self.gy.value() < -140: #Überlegen wie man reichweite von +/- 2 machen kann
                    print(self.s.offset, ColorSensor().reflected_light_intensity)
                    sleep(0.14)
                    self.steer_pair_stop()
                    break
            if self.side_to_follow == -1:
                while i <= count:
                    if self.quit == 1:
                        self.quit = self.forward(self.cm_to_sec(20, 40), 1, 30, opposite)
                        self.side_to_follow = 1
                        i += 30
                    else:
                        self.quit = self.forward(self.cm_to_sec(30, 40), 1, 30, opposite)
                        self.side_to_follow = 1
                        i += 30
            else: 
                while i <= count:
                    if self.quit == 1:
                        self.quit = self.forward(self.cm_to_sec(20, 40), -1, 30, opposite)
                        self.side_to_follow = -1
                        i += 30
                    else:
                        self.quit = self.forward(self.cm_to_sec(30, 40), -1, 30, opposite)
                        self.side_to_follow = -1
                        i += 30

    def forward(self, x, y, count, opposite):
        """Method for driving the robot x seconds forward until LEGOlas reached a crossing"""
        self.s.pid(x, y, 30, opposite)
        sleep(0.05)
            
    def cm_to_sec(self, cm, speed):
        """Function to calculate how many seconds the roboter have to move with speed x to drive n cm"""
        sec = 0.0   
        ref_sec = 2.9
        ref_cm = 1
        ref_speed = 1
        sec = ref_sec * cm / speed
        print('sec: ', sec)
        return sec




