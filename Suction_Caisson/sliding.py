#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 21:56:27 2021

@author: goharshoukat
"""
import math
import numpy as np
def sliding(capacity_cache, cache, soil_type, sand_prop, clay_prop, gamma_m, 
            H_LRP):
    #Input
    #soil_type : str : string specifiying either clay or sand
    #cache     : {}  : dictionary from the precalc function
    ##soil_prop: {}  : dictionary with soil properties of the sub-type 
    #clay_prop : dict : cache with clay proeprties
    #sand_prop : dict : cache with sand proeprties
    #gamma_m   : float : material safety factor
    #H_LRP  : float : m, horizontal load reference point
    h = np.linspace(int(cache['h']), int(cache['h'] + 50), int((cache['h']+50)))   
    if soil_type.lower() == 'clay':    
        Hbase_R = math.pi * cache['D']**2/4 * clay_prop['s_u']
        Hside_R = cache['D'] * h * (h/2 * sand_prop['gamma'] + 2 * 
                                    clay_prop['s_u'])
        
    else:
        phi = math.radians(sand_prop['phi'])
        Hbase_R = capacity_cache['Vbase'] * math.tan(phi)
        kp = (1 + math.sin(phi)) / (1 - math.sin(phi))
        ka = (1 - math.sin(phi)) / (1 + math.sin(phi)) 
        Hside_R = sand_prop['gamma'] * h**2 * cache['D']/2 * (kp - ka)
        
    checker = capacity_cache['Hbase'] + Hside_R/gamma_m > H_LRP
    