#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 17:28:32 2021

@author: goharshoukat


This is the main library description for the suction caisson Foundation design for the 
Selkie Project

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 

Notes: Check with Chris what K is. 
"""
import math
import numpy as np
def capacity_conversions(input_cache, calc_cache, soil_type, soil_prop, K):
    #Input
    #input_cache: {}  : dictionary of user defined inputs 
    #soil_type  : str : string specifiying either clay or sand
    #calc_cache : {}  : dictionary from the precalc function
    #soil_prop  : {}  : dictionary with soil properties of the sub-type 
    #K          : float : to be checked with Chris
    #Output
    #cache : {} : dictionary with 3 important capacity conversion variables
    
    #clay undrained vertical capacity on outside of caisson
    if soil_type.lower() == 'clay':
        Vside = np.pi * calc_cache['D'] * calc_cache['h'] * \
                                        soil_prop['alpha'] * soil_prop['s_u']
        Hside = calc_cache['D'] * calc_cache['h'] * (soil_prop['gamma'] * 
                                 calc_cache['h'] / 2) #equation left incomplete
                                        
    #sand vertical capacity on outside of caisson
    elif soil_type.lower() == 'sand':
        Vside = np.pi * calc_cache['D'] * calc_cache['h']**2 / 2 * K * \
                            soil_prop['gamma'] * math.tan(soil_prop['delta'])
        Ka = (1 + math.sin(soil_prop['phi'])) / (1 - math.sin(soil_prop['phi']))
        Kp = 1 / Ka
        Hside = soil_prop['gamma'] * calc_cache['h'] ** 2 * calc_cache['D'] \
            / 2 * (Kp - Ka)
                                
            
    
    else:
        raise ValueError
        
    

    Hbase = input_cache['H_LRP'] - Hside
    Vbase = input_cache['V_LRP'] + calc_cache['Wc'] - Vside
    hside = 2 * calc_cache['h'] /3 
    Mbase = input_cache['M_LRP'] + hside * Hside + calc_cache['h'] * Hbase
    
    return {'Hbase' : Hbase, 'Vbase' : Vbase, 'Mbase' : Mbase, 'Vside' : Vside}
    