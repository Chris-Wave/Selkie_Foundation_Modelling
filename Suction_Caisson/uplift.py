#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 10:35:24 2021

@author: goharshoukat

Undrained analysis for uplift (tension or anchor based)

Feeds into the Foundation_characteristics
"""
import numpy as np
import math
def uplift(soil_type, analysis_type, capacity_cache, cache , sand_prop, 
           clay_prop, K):
    #Input
    #soil_type : str : string specifiying either clay or sand-drained, sand-undrained
    #cache     : {}  : dictionary from the precalc function
    ##soil_prop: {}  : dictionary with soil properties of the sub-type 
    #clay_prop : dict : cache with clay proeprties
    #sand_prop : dict : cache with sand proeprties
    #analysis_type : str : option to chose between undrained, cavitation-lid and
    #                                                           cavitation-base
    #K         : float : constant user specified
    h = np.linspace(int(cache['h']), int(cache['h'] + 50), int((cache['h']+50)))   
    
    if soil_type.lower() == 'clay':
        if analysis_type.lower() == 'undrained':
            Vult = cache['Wc'] + clay_prop['Nc'] * cache['Ac'] * clay_prop['s_u'] +\
                clay_prop['alpha'] * math.pi * cache['D'] * h * clay_prop['s_u']
        elif analysis_type.lower()=='cavitation-base':
            Vult = math.pi * cache['D']**2 / 4 * h * sand_prop['gamma'] + \
                math.pi * cache['D']**2/4 * (101325 + 1000 * h ) + math.pi * \
                    cache['D'] * clay_prop['alpha'] * h * clay_prop['s_u']
                    
        elif  analysis_type.lower()=='cavitation-lid':
            Vult =  math.pi * cache['D']**2/4 * (101325 + 1000 * h ) + 2 * \
            math.pi * cache['D'] * clay_prop['alpha'] * h * clay_prop['s_u']
        
        else:
            raise ValueError
            
    elif soil_type.lower() == 'sand-undrained':
        if analysis_type.lower() == 'cavitation-base':
            Vult =  math.pi * cache['D']**2 / 4 * h * sand_prop['gamma'] + \
                math.pi * cache['D']**2/4 * (101325 + 1000 * h ) + math.pi * \
                    cache['D'] * sand_prop['gamma'] * h **2/2 * K * math.tan(
                        math.radians(sand_prop['delta']))
                    
            
        elif analysis_type.lower() == 'cavitation-lid':
            Vult =  math.pi * cache['D']**2/4 * (101325 + 1000 * h ) + 2* math.pi * \
                cache['D'] * sand_prop['gamma'] * h **2/2 * K * math.tan(
                    math.radians(sand_prop['delta']))
        
        else:
            raise ValueError
            
    elif soil_type.lower() == 'sand-drained':
        if analysis_type.lower() == 'cavitation-base':
            Vult = math.pi * cache['D']**2/4 * sand_prop['gamma'] * h - \
                math.pi*cache['D']**2/4 * 1000 * h +math.pi * \
                    cache['D'] * sand_prop['gamma'] * h **2/2 * K * math.tan(
                        math.radians(sand_prop['delta']))
                    
        elif analysis_type.lower() == 'cavitation-lid':
           Vult =  2* math.pi * cache['D'] * sand_prop['gamma'] * h **2/2 * K \
               * math.tan(math.radians(sand_prop['delta']))
