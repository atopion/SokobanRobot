#!/usr/bin/env python3
# from pykalman import KalmanFilter
# import numpy as np
# from numpy import ma
# from scipy.stats import norm
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_D, LargeMotor, MoveSteering, MoveTank
from ev3dev2.sensor.lego import ColorSensor
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
        #self.us = UltrasonicSensor()   #shortcut fpr the UltrasonicSensor (looks like a pair of eyes)    
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
        self.cl = ColorSensor() #shortcut for the ColorSensor (points toward the ground)
        self.offset = self.cl.reflected_light_intensity  #Zero point, light reflected, when the ColorSensor detects half white and half black. Each time LEGOlas starts this method new, he calculates the Zeropoint new.


#############################################################################################
#PID Folower and Stop signal								    #
#############################################################################################


    def pid(self, seconds, side_to_follow, count, opposite, back): #side_to_follow is 1 or -1, shows if legolas should follow the right side or the left side of the line (should drive in the inner field)
        """method for line following, for more explainations please take a look at following site: http://www.inpharmix.com/jps/pid_controller_for_lego_mindstorms_robots.html """
        if self.offset < 30 or self.offset > 45:
            self.offset = 30
        kp = 1.3 * side_to_follow
        ki = 0.095 * side_to_follow
        kd = 0.75 * side_to_follow
        Tp = 19.5
        tmp = 0
        integral = 0
        last_error = 0
        derivative = 0
        backwards = 0
        critical_time = 0.039* count #Geschwindigkeit erniedrigkt also auch kritischer Bereich höher angesetzt
        print("count: ", count)
        for i in drange(0,seconds, 0.065): 
            if (1.45 < i and opposite == 1):
                self.steer_pair.off()
                print("Grüne Linie erreicht", self.cl.reflected_light_intensity, i)
                return 1
            tmp = self.cl.reflected_light_intensity
            if backwards == 1 and tmp < 8 and 1.44 < i:
                self.steer_pair.on(0,25)
                time.sleep(0.25)
                print("tmp: ",tmp, "i: ",i)
                self.steer_pair.off()
                return 0
            if (tmp < 10) and seconds - critical_time <= i and backwards == 0:
                    self.steer_pair.on(steering = 0, speed = 25)
                    time.sleep(0.15)
                    print("schwarze linie erreicht", tmp, i)
                    self.steer_pair.off()
                    return 0
            print("offset: ", self.offset," reflected light: ",tmp, "i: ", i)
            error = self.cl.reflected_light_intensity - self.offset
            integral = integral + error
            derivative = error - last_error
            turn = kp * error + ki * integral + kd * derivative
            last_error = error
            if back == 1:
                power_a = (Tp - turn/100) * -1
                power_d = (Tp + turn/100) * -1
                backwards = 1
                self.tank_drive.on(power_a, power_d)
            else:
                self.steer_pair.on(steering = turn, speed = 23)
            time.sleep(0.035)

        self.steer_pair.off()
        self.tank_drive.off()
        return 0
        

#####################################################################################
#SonicSensor									    #
#####################################################################################

#    def box(self):
#        """Method to slow down LEGOlas, whe he meets a box. Uses the UltrasonicSensor"""
#        if self.us.distance_centimeters < 10: #LEGOlas keeps driving forward
#            return True
#        return False

#####################################################################################
#Kalmanfilter								            #	
#####################################################################################

    # def Kalmanfilter(self):
        # kf = KalmanFilter(40)
        # measurements = self.cl.reflected_light_intensity
        # #kf = kf.em(measurements, n_iter=5)
        # (filtered_state_means, filtered_state_covariances) = kf.filter(measurements)
        # (smoothed_state_means, smoothed_state_covariances) = kf.smooth(measurements)
        # print("KF.Filter: ", kf.filter(measurements))
        # print("KF.smooth: ", kf.smooth(measurements))
