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

class Foundation_Definition:
    def __init__(self, weight_concrete, weight_slag, slope, device_geometry):
        #weight_concrete : float   : kN/m**3
        #weight_slab     : float   : kN/m**3
        #slope           : float   : degrees
        #device_geometry : float   : unspecified, Pault to confirm
        self.weight_concrete = weight_concrete
        self.weight_slag = weight_slag
        self.slope = slope
        self.geom = device_geometry #read off the excel. dont know how to use this
        
    el = el    
    def external_loads(self, Mxuls, Myuls, Vuls, Huls):
        #Mxuls : float : kN-m, User-defined
        #Myuls : float : kN-m, User-defined
        #Vuls  : float : kN,   User-defined
        #Huls  : float : kN,   User-defined
        #function to allocate external user defined loads to the foundation
        
        
        
        self.ext_loads_dict = self.el.__func__(self.slope, Mxuls, Myuls, Vuls, 
                                               Huls)
        
    
    """
    declare descriptor to use eccent function for calculations in the eccentric
    function in this class
    """
    def key_calc(self, key: str):
        #function to use to adjust the key calculations
        #key : string : yes, y, all cases permitted. if yes, launches key calculations
        #embed : string : will see at a later s
        
        #lower().startswith() allows all combinations of yes to be accepted
        
       
        if key.lower().startswith('y'):
            self.zs = 0.1 * self.cache_eccent['Ix_min']
        else:
            self.zs = 0
        
        self.Df = self.zs #m
        self.Hs = np.min(self.Df * np.ones(len(self.cache['Calc'])), self.zs + 
                         self.cache['Calc'].t)
        
    eccent = eccent
    def eccentricity(self):
        #function to perform eccentricity calculations. does not need 
        #any arguments. ext_loads dict can be accessed internally
        self.cache_eccent = self.eccent.__func__(self.ext_loads_dict, self.geom)
        
        
        

          
            
x = Foundation_Definition(1000, 100, 5,3)
x.external_loads(0, 0, 10, 10)
loads = x.ext_loads_dict
x.eccentricity()
cache2 = x.cache_eccent

