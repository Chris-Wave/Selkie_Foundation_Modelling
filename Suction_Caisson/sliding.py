#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 21:56:27 2021

@author: goharshoukat


Sliding calculations are performed in this script. This feeds into the foundation_
characteristics class.  

This script includes sliding checker for both clay and sand.  


This is the main library description for the suction caisson Foundation design for the 
Selkie Project

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""
import math
import numpy as np
import logging
def sliding(input_cache, capacity_cache, calc_cache, soil_type, soil, gamma_m,
            gamma_f):
    #Input
     #input_cache: dict {} : dictionary of input cache
     #capacity_cache : dict {} : dictionary of capacity conversion calculations
     #clay       : dict {} : dictionary of clay soil properties
     #calc_cache : dict {} : dictionary of pre calculations
     #gamma_m    : float   : ahrd coded safety factor of material
     #gamma_f    : float   : hard coded favorable safety factor
    logging.info('\n\n**** Sliding Check ****')
    if soil_type.lower() == 'clay':    
        Hbase_R = math.pi * calc_cache['D']**2/4 * soil['s_u']
        Hside_R = calc_cache['D'] * calc_cache['h'] * (calc_cache['h']/2 * 
                                        soil['gamma'] + 2 * soil['s_u'])
        logging.info('\nHbase_R = {}\nHside_R = {}'.format(Hbase_R, Hside_R))                            
        
    else:
        Hbase_R = capacity_cache['Vbase'] * math.tan(soil['phi'])
        kp = (1 + math.sin(soil['phi'])) / (1 - math.sin(soil['phi']))
        ka = (1 - math.sin(soil['phi'])) / (1 + math.sin(soil['phi'])) 
        Hside_R = soil['gamma'] * calc_cache['h']**2 * calc_cache['D']/2 * (kp - ka)
        logging.info('\nHbase_R = {}\nkp = {}\nka = {}\nHside_R = {}'.format(Hbase_R, kp, ka, Hside_R))
        
        
    logging.info('\nSliding Check = {}'.format((Hbase_R + Hside_R)/gamma_m > input_cache['H_LRP'] * gamma_f))
    return (Hbase_R + Hside_R)/gamma_m > input_cache['H_LRP'] * gamma_f
    