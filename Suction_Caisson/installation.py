#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 11:24:48 2021

@author: goharshoukat


Installation calculations are performed in this script. This feeds into the foundation_
characteristics class.  

This script includes 3 functions. installation_clay performs checks for 
clay. installation_sand performs installation checks for sand. 

The function on buckling is used in each of the two above functions to further
ensure installation is passed. 

This is the main library description for the suction caisson Foundation design for the 
Selkie Project

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""

import math
import numpy as np



  
def buckling(input_cache, calc_cache, gamma_m, v, E):
#function to check the buckling limit for installation
    #Inputs
    #input_cache : {}  : dictioinary with input cache    
    #calc_cache  : {}  : dictionary with precalculations
    #gamma_m     : float : safety factor of materials
    #v          : float   : pre-defined, poison ratio
    #E          : float   : young's modulus
    
    #output
    #check      : nd.array : vector with booleans to confirm pass/fail
    psi = 2
    rho = 0.6
    epsilon = 1.04 * np.sqrt(calc_cache['L']**2 / (calc_cache['D']/2 * 
                    calc_cache['L']) * np.sqrt(1 - v**2))
    C = psi * np.sqrt(1 + (rho * epsilon/psi)**2)
    f_E = C * np.pi**2 * E * (input_cache['t']/calc_cache['L'])**2 / (12 * 
                                                                (1 - v**2) )
    
    check = f_E / gamma_m > calc_cache['SL']
    
    return check
    
    
    
def installation_clay(clay, input_cache, calc_cache, v, E, gamma_m, gamma_f):
    #Installation Clay function first solves for installation under self weight
    #In the second step, it solves for the sunction pressure required for the 
    #setting depth
    #Input
    #input_cache: dict {} : dictionary of input cache
    #clay       : dict {} : dictionary of clay soil properties
    #calc_cache : dict {} : dictionary of pre calculations
    #v          : float   : pre-defined, poison ratio
    #E          : float   : young's modulus
    #gamma_m    : float   : ahrd coded safety factor of material
    #gamma_f    : float   : hard coded favorable safety factor
    
    #output
    #check      : {}      : dictionary with pass/fail check for 3 installation
    #checks. self-weight, installed height suction requirement and buckling check


    #Step 1: Self Weight. find the setting height under self weight
    #solve with s = 0
    h_sw_min = 0.1  #minimum self installatino required
    h_sw = (calc_cache['V_comma'] * gamma_f - clay['Nc'] * clay['s_u'] * np.pi *
            calc_cache['D'] * input_cache['t']) / (clay['alpha'] * np.pi * 
            input_cache['D0'] * clay['s_u'] + clay['alpha'] * np.pi * 
            calc_cache['Di'] * clay['s_u'] + clay['gamma'] * np.pi * 
            calc_cache['D'] * input_cache['t'])
    h_sw_checker = h_sw > h_sw_min
         
                  
         
            
    #Step 2. Determine the suction required for the installed depth
    
    Routside = clay['alpha'] * math.pi * input_cache['D0'] * calc_cache['h'] \
                                                                * clay['s_u']
    
    Rinside = clay['alpha'] * math.pi * calc_cache['Di'] * calc_cache['h'] * \
                                                                clay['s_u']

    Rtip = np.pi * calc_cache['D'] * input_cache['t'] * (clay['gamma'] * \
                                calc_cache['h'] + clay['Nc'] * clay['s_u'])
 
    #solve for suction
    s = ((Routside + Rinside + Rtip)- 
         calc_cache['V_comma']) / calc_cache['Ac']
    
    s_checker = s < calc_cache['SL']
    
    
    #buckling check
#    buckling_check = buckling(input_cache, calc_cache, gamma_m, v, E)
    
    return {'sw installation check':h_sw_checker, 
            'suction limit check' : s_checker}

    
    
#import scipy library to solve equations iteratively
from scipy.optimize import fsolve    
from scipy import optimize
def installation_sand(sand, input_cache, calc_cache, v, E, K, gamma_m, gamma_f):
    
    #Installation Clay function first solves for installation under self weight
    #In the second step, it solves for the sunction pressure required for the 
    #setting depth
    #Input
    #input_cache: dict {} : dictionary of input cache
    #sand       : dict {} : dictionary of clay soil properties
    #calc_cache : dict {} : dictionary of pre calculations
    #v          : float   : pre-defined, poison ratio
    #E          : float   : young's modulus
    #K          : float   : u
    #gamma_m    : float   : hard coded safety factor of material
    #gamma_f    : float   : hard coded favorable safety factor
    
    #output
    #check      : {}      : dictionary with pass/fail check for 3 installation
    #checks. self-weight, installed height suction requirement and buckling check


    #Step 1: Self Weight. find the setting height under self weight
    #solve with s = 0
    h_sw_min = 0.1  #minimum self installatino required
    
    #define variables and constants
    m = 1.5 #as specified by OWA doc
    Zi = calc_cache['Di'] / ( 4 * K * math.tan(sand['delta']))
    Z0 = input_cache['D0'] * (m**2 - 1) / ( 4 * K * math.tan(sand['delta']))
    c0 = 0.45
    c1 = 0.36
    c2 = 0.48
    Nq = math.exp(math.pi * math.tan(sand['phi'])) * (math.tan(math.pi/4 + 
                                                        sand['phi']/2))**2
    Ngamma = 1.5 * (Nq - 1) * math.tan(sand['phi'])
    
    
    """
    Need a better implemantation of root finding technique here. 
    Not enough time to sort this out right now
    
    Cant implement a vectorised approach to fsolve. needs a loop. 
    """
    h_sw = []
    for i in calc_cache['V_comma']:
        
        #solve for h iteratively as equation for s is implicit. 
        def func(h):
            Routside =  sand['gamma'] * Z0**2 * (math.exp(h / Z0) - 1 - (h / Z0)) * (
                K * math.tan(sand['delta'])) * (math.pi * input_cache['D0'])
            
            Rinside = sand['gamma'] * Zi**2 * (math.exp(h / Zi) - 1 - h / Zi) * (
                K * math.tan(sand['delta'])) * math.pi * calc_cache['Di']
            
            Rtip =  (sand['gamma'] * Zi * (math.exp(h / Zi) - 1) * Nq +
                     sand['gamma'] * input_cache['t'] * Ngamma) *  math.pi * \
                        calc_cache['D'] * input_cache['t']
                        
            return (Routside + Rinside + Rtip) - i
        
        h_sw = np.append(h_sw, fsolve(func, 1))
        h_sw_checker = h_sw > h_sw_min
    
    
    
    #Step 2: Calculate if the Sl is violated with different skirt lengths
    #h is now a vector calculated from calc_cache
    a = c0 - c1 * (1 - np.exp(-calc_cache['h']/(c2 * calc_cache['D'])))

    
    """
    Need a better implemantation of root finding technique here. 
    Not enough time to sort this out right now
    
    Cant implement a vectorised approach to fsolve. needs a loop. 
    
    Calculation for suction required for different h values
    since this is a vector, needs a for loop. 
    """
    s = []
    for i in range(len(calc_cache['h'])):
        def func2(s):
            
            Routside = (sand['gamma'] + (a[i] * s / calc_cache['h'][i])) * Z0**2 * (
                np.exp(calc_cache['h'][i] / Z0) - 1 - calc_cache['h'][i] / Z0)\
                * (K * math.tan(sand['delta'])) * math.pi * input_cache['D0']
            
            Rinside = (sand['gamma'] - (((1 - a[i]) * s) / calc_cache['h'][i])) * \
                Zi**2 * (np.exp(calc_cache['h'][i] / Zi) - 1 - 
                         (calc_cache['h'][i] / Zi))\
                * (K * math.tan(sand['delta'])) * math.pi * calc_cache['Di']
            
            Rtip = ((sand['gamma'] - (((1 - a[i]) * s) / calc_cache['h'][i])) * Zi * (
                np.exp(calc_cache['h'][i] / Zi) - 1) * Nq + sand['gamma'] * 
                input_cache['t'] * Ngamma) * math.pi * input_cache['t'] * calc_cache['D']
            
            #solving for suction - s
# =============================================================================
            return ((Routside + Rtip + Rinside)  - 
            calc_cache['V_comma'][i]) / calc_cache['Ac']

            
        s =  fsolve(func2, 0)
        print('s = {}'.format(s))
        s_checker = s < calc_cache['SL'] 
    
    #buckling check
   # buckling_check = buckling(input_cache, calc_cache, gamma_m, v, E)
    
    return {'sw installation check' : h_sw_checker,
            'suction limit check' : s_checker}