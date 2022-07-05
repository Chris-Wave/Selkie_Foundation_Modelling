#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 19:41:59 2021

@author: goharshoukat


This function calculates the sliding resistance
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
def sliding_resistance(c, loads, eccent_cache, weight, phi, slope, Hs, SF):
    #Inputs
    #c           : float   : kPa, cohesion/safety factor
    #Loads       : {} dict : dictionary of the loads adjusted for slope
    #eccnt_cache : {} dict : dictionary with eccentricity calculations for multiple dimensions
    #weight      : float   : kN/m3, weight of soil
    #phi         : float   : degrees, obtained from the friction angle of soil
    #slope       : float   : degrees
    #Hs     : float : m, Side soil contact
    #SF     : float : safety factor for bearing capacity
    
    #output
    #checker_sliding : pd.Series : series of booleans for dims that pass the 
    #design check necessary for sliding resistance
    phi = math.radians(phi)
    slope = math.radians(slope)
    Hu_undrained = eccent_cache['Calc'].A * c + ((loads['Vv']/eccent_cache['Calc'].A * math.cos(slope)) *
                             math.tan(phi)*eccent_cache['Calc'].A)#+2 *Hs * eccent_cache['Calc'].L*c 
    #Hu_drained = np.ones(len(Hu_undrained)) * ((loads['Vv']/eccent_cache['Calc'].A * math.cos(slope)) *
    #                         math.tan(phi)*eccent_cache['Calc'].A)
    
    sliding_force = (loads['Vv']) * math.sin(slope) + (
                         loads['Vh'] * math.cos(slope)) 
    #Hu_drained_SF = np.abs(Hu_drained/SF)
    Hu_undrained_SF = Hu_undrained / SF
    
    return (np.min([Hu_undrained_SF], axis = 0) > sliding_force)
    
    
    
    
    
                         
    
    