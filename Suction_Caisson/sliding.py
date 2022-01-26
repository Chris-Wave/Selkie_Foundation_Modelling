#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 21:56:27 2021

@author: goharshoukat
"""
import math
import numpy as np
def sliding(input_cache, capacity_cache, calc_cache, soil_type, soil, gamma_m):
    #Input
    #soil_type : str : string specifiying either clay or sand
    #cache     : {}  : dictionary from the precalc function
    ##soil_prop: {}  : dictionary with soil properties of the sub-type 
    #clay_prop : dict : cache with clay proeprties
    #sand_prop : dict : cache with sand proeprties
    #gamma_m   : float : material safety factor
    #H_LRP  : float : m, horizontal load reference point   
    if soil_type.lower() == 'clay':    
        Hbase_R = math.pi * calc_cache['D']**2/4 * soil['s_u']
        Hside_R = calc_cache['D'] * calc_cache['h'] * (calc_cache['h']/2 * 
                                        soil['gamma'] + 2 * soil['s_u'])
                                    
        
    else:
        phi = soil['phi']
        Hbase_R = capacity_cache['Vbase'] * math.tan(soil['phi'])
        kp = (1 + math.sin(soil['phi'])) / (1 - math.sin(soil['phi']))
        ka = (1 - math.sin(soil['phi'])) / (1 + math.sin(soil['phi'])) 
        Hside_R = soil['gamma'] * calc_cache['h']**2 * calc_cache['D']/2 * (kp - ka)
        
    return capacity_cache['Hbase'] + Hside_R/gamma_m > input_cache['H_LRP']
    