#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 17:28:32 2021

@author: goharshoukat

Only soil is an acceptable soil_type until further releases
incomplete function
"""
import math

def capacity_conversions(soil_type, cache, soil_prop, K, H_LRP, V_LRP, M_LRP):
    #Input
    #soil_type : str : string specifiying either clay or sand
    #cache     : {}  : dictionary from the precalc function
    ##soil_prop: {}  : dictionary with soil properties of the sub-type 
    #K         : float : constant, fixed
    #V_LRP  : float : m, vertical load reference point
    #H_LRP  : float : m, horizontal load reference point
    #M_LRP  : float : m, moment load reference point
    
    #Output
    #cache : {} : dictionary with 3 important capacity conversion variables
    
    #clay undrained vertical capacity on outside of caisson
    if soil_type.lower() == 'clay':
        raise ValueError
        #Vside = math.pi * cache['D'] * cache['h'] * \
        #                                soil_prop['alpha'] * soil_prop['s_u']
                                        
    #sand vertical capacity on outside of caisson
    else:
        Vside = math.pi * cache['D'] * cache['h']**2 / 2 * K * \
                            soil_prop['gamma'] * math.tan(soil_prop['delta'])
    
    Hside = cache['D'] * Cache['h'] * (soil['gamma'] * cache['h'] / 2) #equation left incomplete
    Hbase = Hside - H_LRPVbase
    Vbase = V_LRP + cache['Wc'] - Vside
    hside = 2 * cache[h] /3 
    Mbase = M_LRP + hside * Hside + cache['h'] * Hbase
    
    return {'Hbase' : Hbase, 'Vbase' : Vbase, 'Mbase' : Mbase}