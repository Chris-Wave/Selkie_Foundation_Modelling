#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 11:19:25 2021

@author: goharshoukat

This is one of the header files for the Gravity based Foundation design for the 
Selkie Project

It is based off of Paul Bonar's adaptation of Majid Hussain's work. 

Undrained and Drained Soil Properties classes are declared

For details about the methodology, contact pbonar@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""


"""
file redundant. merged into foundation_characteristics. 
"""
from bearing_capacity import drained_bearing_capacity
import math
from foundation_characteristics import Foundation_Definition
#Class to clasify soil. all parameters to be user defined, no default initially
#all standard units used
#angles in degree  
class Drained_Soil:
    def __init__(self, friction_angle, cohesion, fos, sensitivity):
        #friction_angle         : float : angle in degrees, obtained from lookup table. 
        #cohesion               : float : value in kPa
        #fos (factor of safety) : float :
        #sensititivity          : TBD with Paul : 
        
            
        self.friction_angle = friction_angle                #degrees            
        self.cohesion = cohesion                            #kPa
        self.fos = fos                                      #fos is for soil parameters
        self.sensitivity = sensitivity
        """
        for calculations, all angles need to be converted to radians, and 
        then reconverted back to degrees.
        
        The code is based off on degrees. 
        """
        self.phi = math.degrees(math.atan(math.tan(
            math.radians(self.friction_angle))/self.fos))   #degrees
        self.c = self.cohesion/self.fos                     #kPa
        
        
class Undrained_Soil:
        def __init__(self, friction_angle, cohesion, fos, relative_density, 
                     weight, sensitivity):
            #friction_angle         : float : angle in degrees, obtained from lookup table. 
            #cohesion               : float : value in kPa
            #fos (factor of safety) : float : 
            #relative_density       : float : %, obtained from the look-up table, user defined 
            #Weight of soil         : float : kN/m**3, Weight of soil
            #sensititivity          : TBD with Paul : 
                
                
            self.friction_angle = friction_angle                #degrees            
            self.cohesion = cohesion                            #kPa
            self.fos = fos                                      #fos is for soil parameters
            self.relative_density = relative_density            #  %
            self.weight = weight                                #kN/m**3
            self.sensitivity = sensitivity
            """
            for calculations, all angles need to be converted to radians, and 
            then reconverted back to degrees.
            
            The code is based off on degrees. 
            """
            self.phi = math.degrees(math.atan(math.tan(
                math.radians(self.friction_angle))/self.fos))   #degrees
            self.c = self.cohesion/self.fos                     #kPa
            
            