#!/usr/bin/env python3
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_D, LargeMotor, MoveSteering
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor   
from Robot import Robot   

class Sensors():
    """Class to use the senosors for line following, moving slower and detecting final boxes"""

    def __init__(self):
        """init method declares all shortcuts for the sensors and declares the name for the steer_pair (see Robot.py)"""
        self.steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class = LargeMotor) # steer_pair moves the robot
        self.us = UltrasonicSensor()   #shortcut fpr the UltrasonicSensor (looks like a pair of eyes)    
        self.cl = ColorSensor() #shortcut for the ColorSensor (points toward the ground)
        self.r = Robot() #shortcut for Robot (Robot implements the movements)

    def pid(self):
        """Method for Line Following, for more explainations please take a look at following site: http://www.inpharmix.com/jps/PID_Controller_For_Lego_Mindstorms_Robots.html """
        kp = 1 
        ki = 0.05  
        kd = 0.5
        offset = self.cl.reflected_light_intensity  #Zero point, light reflected, when the ColorSensor detects half white and half black. Each time LEGOlas starts this method new, he calculates the Zeropoint new.
        integral = 0
        last_error = 0
        derivative = 0
        for i in range (0, 250):
            error = self.cl.reflected_light_intensity - offset
            integral = integral + error
            derivative = error - last_error
            Turn = kp * error + ki * integral + kd * derivative 
            self.steer_pair.on(steering = Turn, speed = 50)
            last_error = error
            print('Turn = %d, error = %d, integral = %f, derivative = %f'%(Turn, error, integral, derivative))

        self.steer_pair.off()

    def box(self):
        """Method to slow down LEGOlas, whe he meets a box. Uses the UltrasonicSensor"""
        while self.us.distance_centimeters < 300: #LEGOlas jeeps driving forward
            print(self.us.distance_centimeters)
            self.steer_pair.on(0, 50) #Driving forward (see steering = 0) with speed 50
            if self.us.distance_centimeters < 30: #When LEGOlas detecs an object he reduces his speed
                self.steer_pair.on(0, 25)
            if self.us.distance_centimeters > 30: #Is the Object out of the way, he gets faster
                self.steer_pair.on(0, 50)   
