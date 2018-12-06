#!/usr/bin/env python3
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_D, LargeMotor, MoveSteering
from ev3dev2.sensor.lego import GyroSensor
from time import sleep
from Directions import  Directions

class Robot():
#"""Class for roboter movements."""
    
    def __init__(self):
        """Constructor for the internal state of the robot, e.g. in which direction he is
        currently looking"""
        self.direction = Directions.up
        self.gy = GyroSensor()
        self.steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class= LargeMotor)

    def gyro_reset(self):
        """Method to reset the GyroSensor to 0"""
        self.gy.mode = 'GYRO-RATE'
        self.gy.mode = 'GYRO-ANG'

    def steer_pair_l(self):
        """Method to initalise the steering to the right side with speed set to 100"""
        self.steer_pair.on(steering=-100, speed=100)

    def steer_pair_r(self):
        """Method to initalise the steering to the left side with speed set to 100"""
        self.steer_pair.on(steering=100, speed=100)

    def steer_pair_stop(self):
        self.steer_pair.off(True)

    def turn(self, direction):
        """Method to calculate the right degree to turn. LEGOlas can move in the directions Up, Down, LEft, Right"""
        self.gyro_reset()
        degrees_to_turn = self.direction - direction
        print(degrees_to_turn)
        if degrees_to_turn == 0:
            self.forward(2)
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
        func()
        print(direction)
        self.direction = direction
        print(self.direction)

    def turn_right(self):
        """Method to turn LEGOlas 90° to the right"""
        self.gyro_reset()
        self.steer_pair_r()
        while self.gy.value() < 200:
            if self.gy.value() > 87:
                self.steer_pair_stop()
                break
        self.forward(2)
    
    def turn_left(self):
        """Method to turn LEGOlas 90° to the left"""
        self.gyro_reset()
        self.steer_pair_l()
        while self.gy.value() > -200:
            print(self.gy.value())
            if self.gy.value() < -80:
                self.steer_pair_stop()
                break
        self.forward(2)
    
    def turn_back(self):
        """Method to turn LEGOlas 180° around"""
        self.gyro_reset()
        self.steer_pair_r()
        while self.gy.value() < 200:
            if self.gy.value() > 177:
                print(self.gy.value())
                self.steer_pair_stop()
                break
        self.forward(2)

    def forward( self, x):
        """Method for driving the robot x seconds forward"""
        self.steer_pair.on_for_seconds(steering=0, speed=50, seconds=x)
        sleep(1)

    def commands(self, str):
        for i in str:
            if i == 'l':
                self.turn(Directions.left)
            if i == 'r':
                self.turn(Directions.right)
            if i == 'u':
                self.turn(Directions.up)
            if i == 'd':
                self.turn(Directions.down)
            
