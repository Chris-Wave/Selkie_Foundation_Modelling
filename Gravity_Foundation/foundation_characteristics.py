#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 15:47:51 2021

@author: goharshoukat

Foundation properties and material characteristics are defined in this class. 

This is one of the header files for the Gravity based Foundation design for the 
Selkie Project

It is based off of Paul Bonar's adaptation of Majid Hussain's work. 



For details about the methodology, contact pbonar@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""
from Eccentricity import eccent
from ext_loads_func import external_loads as el
import math
import numpy as np
from bearing_capacity import bearing_capacity
from sliding import sliding_resistance
from overturning_resistance import overturning


class Foundation_Definition:
    def __init__(self, weight_concrete, weight_slag, slope, device_geometry, SF,
                 thickness_factor = 0.3, concrete_density = 24):
        #weight_concrete : float   : kN/m**3
        #weight_slab     : float   : kN/m**3
        #slope           : float   : degrees
        #device_geometry : float   : unspecified, Pault to confirm
        #SF              : float   : safety factor for beariing capacity
        #thickness_factor: float   : thickness factor
        
        self.weight_concrete = weight_concrete
        self.weight_slag = weight_slag
        self.slope = slope
        self.geom = device_geometry #read off the excel. dont know how to use this
        self.SF = SF
        self.tf = thickness_factor
        self.concrete_density = concrete_density
        
    def drained_soil(self, friction_angle, cohesion, fos, sensitivity, weight):
        #friction_angle         : float : angle in degrees, obtained from lookup table. 
        #cohesion               : float : value in kPa
        #fos (factor of safety) : float :
        #weight                 : float : weight of soil kN/m**3
        #sensititivity          : TBD with Paul : 
        
            
        self.friction_angle = friction_angle                #degrees            
        self.cohesion = cohesion                            #kPa
        self.fos = fos                                      #fos is for soil parameters
        self.sensitivity = sensitivity
        self.weight = weight
        """
        for calculations, all angles need to be converted to radians, and 
        then reconverted back to degrees.
        
        The code is based off on degrees. 
        """
        self.phi = math.degrees(math.atan(math.tan(
            math.radians(self.friction_angle))/self.fos))   #degrees
        self.c = self.cohesion/self.fos                     #kPa
        
    def undrained_soil(self, friction_angle, cohesion, fos, relative_density, 
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
            
        
    el = el    
    def external_loads(self, Mxuls, Myuls, Vuls, Huls):
        #Mxuls : float : kN-m, User-defined
        #Myuls : float : kN-m, User-defined
        #Vuls  : float : kN,   User-defined
        #Huls  : float : kN,   User-defined
        #function to allocate external user defined loads to the foundation
        self.Vuls = Vuls
        self.Huls = Huls
        
        #horizontal and vertical loads adjusted for slope, passed to 
        self.ext_loads_dict = self.el.__func__(self.slope, Mxuls, Myuls, Vuls, 
                                               Huls)
        

        
    
    """
    declare descriptor to use eccent function for calculations in the eccentric
    function in this class
    """
    def key_calc(self, key: str):
        #function to use to adjust the key calculations
        #key : string : yes, y, all cases permitted. if yes, launches key calculations
        
        #lower().startswith() allows all combinations of yes to be accepted
        
       
        if key.lower().startswith('y'):
            self.zs = 0.1 * self.cache_eccent['Ix_min']
        else:
            self.zs = 0
        
        self.Df = self.zs #m
        self.Hs = np.min([self.Df, 
                         self.zs], axis = 0)
        
    
    def embedment(self, embed: str):
        #function to specify if embedment is present or not. 
        self.embed = embed
        
        
    eccent = eccent
    def eccentricity(self):
        #function to perform eccentricity calculations. does not need 
        #any arguments. ext_loads dict can be accessed internally
        #shift this into the external loads function. 
        self.cache_eccent = self.eccent.__func__(self.ext_loads_dict, self.geom,
                                                 tf = self.tf, 
                                                 concrete_density = self.concrete_density)
        
    
    def design_check(self):
        #variable will be used for comparing design validity only after 
        #bearing_capacity function returns the bearing capacity
        #function different from slope adjusted values.
        slope = math.radians(self.slope)
        self.load_check = (self.Vuls - self.cache_eccent['Calc'].Wb -  
                           self.cache_eccent['Calc'].A * self.zs * self.weight) * (
                               math.cos(slope)) + self.Huls * math.sin(slope)
        
        #call function bearing_capacity   
        #assign it to a column in the diimensions dataframe  
        #if else statement
        if self.embed.lower().startswith('y'):                  
            self.cache_eccent['Calc']['bearing_checker'] = bearing_capacity(
                                      self.phi, self.ext_loads_dict, 
                                      self.load_check, self.c, self.geom, 
                                      self.weight, self.Df, self.Hs, 
                                      self.sensitivity, self.SF,
                                      embed = True)
        else:
            self.cache_eccent['Calc']['bearing_checker'] = bearing_capacity(
                                      self.phi, self.ext_loads_dict, 
                                      self.load_check, self.c, self.geom, 
                                      self.weight, self.Df, self.Hs, self.SF)
            
            
        
        
        
        #call function sliding_Resistance to check design for sliding resistance
        self.cache_eccent['Calc']['sliding_checker'] = sliding_resistance(
                                             self.c, self.ext_loads_dict,
                                             self.cache_eccent, self.weight, 
                                             self.phi, self.slope, self.Hs, 
                                             self.SF)
        
        
        self.cache_eccent['Calc']['overturning_checker'] = overturning(
                                          self.ext_loads_dict, 
                                          self.cache_eccent, self.slope,
                                          self.SF)
        
        
       
        
        return self.cache_eccent