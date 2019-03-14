#!/usr/bin/env python3
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_D, LargeMotor, MoveSteering
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor   
import time

def drange(start, stop, step):
    while start < stop:
        yield start
        start += step


class Sensors():
    """Class to use the senosors for line following, moving slower and detecting final boxes"""

    def __init__(self):
        """init method declares all shortcuts for the sensors and declares the name for the steer_pair (see Robot.py)"""
        self.steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class = LargeMotor) # steer_pair moves the robot
        self.us = UltrasonicSensor()   #shortcut fpr the UltrasonicSensor (looks like a pair of eyes)    
        self.cl = ColorSensor() #shortcut for the ColorSensor (points toward the ground)
        self.offset = self.cl.reflected_light_intensity  #Zero point, light reflected, when the ColorSensor detects half white and half black. Each time LEGOlas starts this method new, he calculates the Zeropoint new.


    def pid(self, seconds, side_to_follow, count): #side_to_follow is 1 or -1, shows if LEGOlas should follow the right side or the left side of the line (should drive in the inner field)
        """Method for Line Following, for more explainations please take a look at following site: http://www.inpharmix.com/jps/PID_Controller_For_Lego_Mindstorms_Robots.html """
        kp = 1 * side_to_follow
        ki = 0.025 * side_to_follow
        kd = 0.5 * side_to_follow
        integral = 0
        last_error = 0
        derivative = 0
        compare = 0
        critical_time = 0.020* count 
        print("Count: ", count)
        for i in drange(0,seconds, 0.08): 
            if seconds - critical_time <= i: #Seconden anpassen und gucken wie häufig man gerade aus fährt, damit ich die if methode länger machen 
            #    print("Kritischer Bereich")
                while (self.cl.reflected_light_intensity <= self.offset-18):
                    self.steer_pair.on(steering = 0, speed = 40)
                    time.sleep(0.15)
                    print("Schwarze Linie erreicht", i)
                    self.steer_pair.off()
                    compare += 1
                    break
            if compare > 0:
                break
            else:
                print("Offset: ", self.offset," Reflected Light: ",self.cl.reflected_light_intensity, "i: ", i)
                error = self.cl.reflected_light_intensity - self.offset
                integral = integral + error
                derivative = error - last_error
                Turn = kp * error + ki * integral + kd * derivative 
                self.steer_pair.on(steering = Turn, speed = 40)
                last_error = error
                #print("integral: %.2f, derivative: %.2f, Turn: %.2f", integral, derivative, Turn)
                time.sleep(0.05)

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
