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
def installation_clay(sand, clay, cache, D0, t):
    #Input
    #sand  : dict {} : dictionary of sand soil properties
    #clay  : dict {} : dictionary of clay soil properties
    #cache : dict {} : dictionary of pre calculations
    #D0    : float : m, user specified value of outer dia
    
    #array of different installed deepths checked
    h = np.linspace(int(cache['h']), int(cache['h'] + 50), int((cache['h']+50)))

    Routside = clay['alpha'] * math.pi * D0 * h * clay['s_u']

    Rinside = clay['alpha'] * math.pi * cache['Di'] * h * clay['s_u']

    Rtip = math.pi * cache['D'] * t * (sand['gamma'] * h + 
                                                clay['Nc'] * clay['s_u'])
    
    Rtotal = Routside + Rinside + Rtip
    
    force_differential = Rtotal - cache['V_comma']  #donward - upward force
    
    suction_applied = cache['SL'] * cache['Ac']
    suction_differential = Rtotal + suction_applied
    

def installation_sand(sand, clay, cache, D0, K, t):
    delta = math.radians(sand['delta'])
    Zi = cache['Di'] / ( 4 * K * math.tan(delta))
    Z0 = D0 / ( 4 * K * math.tan(delta))
    c0 = 0.45
    c1 = 0.36
    c2 = 0.48
    s = 0
    h = np.linspace(int(cache['h']), int(cache['h'] + 50), int((cache['h']+50)))
    a = c0 - c1(1 - np.exp(-h/(c2*cache['D'])))
    
    phi = math.radians(sand['phi'])
    Nq = math.exp(math.pi * math.tan(phi)) * (math.tan(math.pi/4 + phi/2))**2
    Routside = (sand['gamma'] + a * s / h) * Z0**2 * (
        np.exp(h/Z0) - 1 - h/Z0) * K * math.tan(delta) * math.pi * D0
    
    Rinside = (sand['gamma'] - a * s / h) * Zi**2 * (
        np.exp(h/Zi) - 1 - h/Zi) * K * math.tan(delta) * math.pi * cache['Di']
    
    Rtip = ((sand['gamma'] - a * s / h) * Zi * (np.exp(h/Zi) - 1) * Nq + 
            sand['gamma'] * t * Nq) * (math.pi * cache['D'] * t)
    
    Rtotal = Routside + Rinside + Rtip
    force_differential = Rtotal - cache['V_comma']
    
    suction_applied = cache['SL'] * cache['Ac']
    suction_differential = Rtotal + suction_applied
    
    
def buckling(cache, v, L, t, E, gamma_m):
    #Inputs
    #cache      : {}  : dictionary with precalculations
    #v          : float : nu, poissons ration
    #L          : float : skirt length
    #t          : float : wall thickness
    #E          : float : Young's Modulus
    #gamma_m    : float : safety factor of materials
    #
    #
    psi = 2
    rho = 0.6
    epsilon = 1.04 * math.sqrt(L**2 / (cache['D']/2 * t) * math.sqrt(1 - v**2))
    C = psi * math.sqrt(1 + (rho * epsilon/psi)**2)
    f_E = C * math.pi**2 * E * (t/L)**2 / (12 * (1 - v**2) )
    
    check = f_E / gamma_m > cache['SL']
    
    
    
    

    
    
    
    
    
