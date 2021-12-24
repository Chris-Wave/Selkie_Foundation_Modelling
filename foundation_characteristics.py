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
import math
from Eccentricity import eccent

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
        

    def external_loads(self, Mxuls, Myuls, Vuls, Huls):
        #Mxuls : float : kN-m, User-defined
        #Myuls : float : kN-m, User-defined
        #Vuls  : float : kN,   User-defined
        #Huls  : float : kN,   User-defined
        #function to allocate external user defined loads to the foundation
        
        #adjust the Vuls and Huls by taking the slope effects into account
        
        #horizontal load (kN)
        Vh = Huls * math.cos(math.radians(self.slope)) - \
             Vuls * math.sin(math.radians(self.slope))
             
        #vertical load (kN)
        Vv = Huls * math.sin(math.radians(self.slope)) + \
             Vuls * math.cos(math.radians(self.slope))
        
        self.ext_loads_dict = {'Mxuls':Mxuls, 'Myuls':Myuls, 'Vv':Vv, 
                          'Vh':Vh}
    
    """
    declare descriptor to use eccent function for calculations in the eccentric
    function in this class
    """
    eccent = eccent
    def eccentricity(self):
        #function to perform eccentricity calculations. does not need 
        #any arguments. ext_loads dict can be accessed internally
        
        self.ex = self.ext_loads_dict['Mxuls'] / self.ext_loads_dict['Vv'] # unit (m)
        self.ey = self.ext_loads_dict['Myuls'] / self.ext_loads_dict['Vv'] # unit (m)
        self.Ix_min = max(6 * self.ex, self.geom) #might need tweaking
        self.Iy_min = max(6 * self.ey, self.goem)
        self.cache_eccent = self.eccent.__func__(self.ex, self.ey, 
                                            self.Ix_min, self.Iy_min)
        
        
        
        
    def key_calc(self, key: str):
        #function to use to adjust the key calculations
        #key : string : yes, y, all cases permitted. if yes, launches key calculations
        #embed : string : will see at a later s
        
        #lower().startswith() allows all combinations of yes to be accepted
        
       """
        if key.lower().startswith('y'):
            self.zs = 0.1 * self.Ix
        else:
            self.zs = 0
       """
       pass            
            
    
x = Foundation_Definition(100, 1010, 5, 3)