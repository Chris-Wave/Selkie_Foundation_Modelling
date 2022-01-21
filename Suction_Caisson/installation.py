#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 11:24:48 2021

@author: goharshoukat


Installation calculations are performed in this script. This feeds into the foundation_
characteristics class.  

Not sure what to return or how to incorporate this in the code

This is the main library description for the suction caisson Foundation design for the 
Selkie Project

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""
import math
import numpy as np
def installation_clay(clay, input_cache, calc_cache, gamma_m, gamma_f):
    #Installation Clay function first solves for installation under self weight
    #In the second step, it solves for the sunction pressure required for the 
    #setting depth
    #Input
    #input_cache: dict {} : dictionary of input cache
    #clay       : dict {} : dictionary of clay soil properties
    #calc_cache : dict {} : dictionary of pre calculations
    #D0         : float : m, user specified value of outer dia
    
    #Step 1: Self Weight. find the setting height under self weight
    #solve with s = 0
    h_sw_min = 0.1  #minimum self installatino required
    h_sw = (calc_cache['V_comma'] * gamma_f - clay['Nc'] * clay['Su'] * np.pi *
            calc_cache['D'] * input_cache['t']) / (clay['alpha'] * np.pi * 
            input_cache['D0'] * clay['s_u'] + clay['alpha'] * np.pi * 
            calc_cache['Di'] * clay['s_u'] + clay['gamma'] * np.pi * 
            calc_cache['D'] * input_cache['t'])
             
              
    
    
    #array of different installed deepths checked
    h = np.linspace(int(calc_cache['h']), int(calc_cache['h'] + 50), int((calc_cache['h']+50)))

    Routside = clay['alpha'] * math.pi * D0 * h * clay['s_u']

    Rinside = clay['alpha'] * math.pi * calc_cache['Di'] * h * clay['s_u']

    Rtip = math.pi * calc_cache['D'] * t * (sand['gamma'] * h + 
                                                clay['Nc'] * clay['s_u'])
    
    Rtotal = Routside + Rinside + Rtip
    
    force_differential = Rtotal - calc_cache['V_comma']  #donward - upward force
    
    suction_applied = calc_cache['SL'] * calc_cache['Ac']
    suction_differential = Rtotal + suction_applied
    

def installation_sand(sand, clay, calc_calc_cache, D0, K, t):
    delta = math.radians(sand['delta'])
    Zi = calc_calc_cache['Di'] / ( 4 * K * math.tan(delta))
    Z0 = D0 / ( 4 * K * math.tan(delta))
    c0 = 0.45
    c1 = 0.36
    c2 = 0.48
    s = 0
    h = np.linspace(int(calc_calc_cache['h']), int(calc_calc_cache['h'] + 50), int((calc_calc_cache['h']+50)))
    a = c0 - c1(1 - np.exp(-h/(c2*calc_calc_cache['D'])))
    
    phi = math.radians(sand['phi'])
    Nq = math.exp(math.pi * math.tan(phi)) * (math.tan(math.pi/4 + phi/2))**2
    Routside = (sand['gamma'] + a * s / h) * Z0**2 * (
        np.exp(h/Z0) - 1 - h/Z0) * K * math.tan(delta) * math.pi * D0
    
    Rinside = (sand['gamma'] - a * s / h) * Zi**2 * (
        np.exp(h/Zi) - 1 - h/Zi) * K * math.tan(delta) * math.pi * calc_calc_cache['Di']
    
    Rtip = ((sand['gamma'] - a * s / h) * Zi * (np.exp(h/Zi) - 1) * Nq + 
            sand['gamma'] * t * Nq) * (math.pi * calc_calc_cache['D'] * t)
    
    Rtotal = Routside + Rinside + Rtip
    force_differential = Rtotal - calc_calc_cache['V_comma']
    
    suction_applied = calc_calc_cache['SL'] * calc_calc_cache['Ac']
    suction_differential = Rtotal + suction_applied
    
    
def buckling(calc_calc_cache, v, L, t, E, gamma_m):
    #Inputs
    #calc_calc_cache      : {}  : dictionary with precalculations
    #v          : float : nu, poissons ration
    #L          : float : skirt length
    #t          : float : wall thickness
    #E          : float : Young's Modulus
    #gamma_m    : float : safety factor of materials
    #
    #
    psi = 2
    rho = 0.6
    epsilon = 1.04 * math.sqrt(L**2 / (calc_calc_cache['D']/2 * t) * math.sqrt(1 - v**2))
    C = psi * math.sqrt(1 + (rho * epsilon/psi)**2)
    f_E = C * math.pi**2 * E * (t/L)**2 / (12 * (1 - v**2) )
    
    check = f_E / gamma_m > calc_calc_cache['SL']
    
    
    
    

    
    
    
    
    
