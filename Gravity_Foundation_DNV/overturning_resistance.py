#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 10:57:59 2021

@author: goharshoukat


This function calculates the overturning resistance
This file feeds into foundation_characteristics

This will be used as a descriptor for the above class

THis script is part of the Selkie Project

It is based off of Paul Bonar's adaptation of Majid Hussain's work. 

The drained analysis makes use of the Meyerhof's methodology'
For details about the methodology, contact pbonar@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""

import math
import numpy as np

def overturning(loads, eccent_cache, slope, SF):
    #Inputs
    #Loads       : {} dict : dictionary of the loads adjusted for slope
    #eccent_cache : {} dict : dictionary with eccentricity calculations for multiple dimensions
    #slope       : float   : degrees
    #SF     : float : safety factor for bearing capacity
    
    #output
    #checker_overturning : pd.Series : series of booleans for dims that pass the 
    #design check necessary for overturning resistance
    
    slope = math.radians(slope)
    
    Vuls_down = loads['Vv']
    
    resistance = (Vuls_down) * math.cos(slope) * \
        eccent_cache['Calc'].B / 2
    
    overturning_moment = loads['Mxuls']
    resistance_SF = resistance/SF
    
    checker = resistance_SF > overturning_moment
    return checker
    
        

