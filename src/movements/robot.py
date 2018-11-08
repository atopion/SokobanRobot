#!/usr/bin/env python3
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_D, LargeMotor
from time import Sleep

class robot():
"""Class for roboter movements."""

    def turn_right():
        """Method to turn the robot 90° to the right side"""
        steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class=LargeMotor)
        steer.pair.on_for_degrees(steering=-100, speed=50, degrees=575)
        sleep(1)

    
    def turn_left():
        """Method to turn the robot 90° to the left side"""
        steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class=LargeMotor)
        steer.pair.on_for_degrees(steering=100, speed=50, degrees=575)
        sleep(1)
    
    def turn_back():
        """Method to turn the robot 180° to the left side"""
        steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class=LargeMotor)
        steer.pair.on_for_degrees(steering=100, speed=50, degrees=1150)
        sleep(1)

    def forward(int x):
        """Method for driving the robot x seconds forward"""
        steering_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class=LargeMotor)
        steering_pair.on_for_seconds(steering=0, speed=50, seconds=x)
        sleep(1)
