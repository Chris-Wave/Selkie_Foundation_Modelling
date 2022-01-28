#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:36:44 2021

@author: goharshoukat

Prelim calculations are performed in this script. This feeds into the foundation_
characteristics class.  

This is the main library description for the suction caisson Foundation design for the 
Selkie Project

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""
import math
import numpy as np

def precalculations(input_cache, rhosteel, rhowater):
    #input
    #input_cache : {} dict : dict of floats with user inputs as cache 
    #rhosteel : float : kg/m**3, density of steel
    #rhowater : flat : kg/m**3, water density
    
    #output
    #cache : dict: dictionary with results of all the below calculations
    
    L = np.arange(input_cache['Lmin'],input_cache['Lmax'], input_cache['Ldelta'])
    h = L - 0.5                     #installed depth
    Di = input_cache['D0'] - 2 * input_cache['t']                #inner dia
    D = (Di + input_cache['D0']) / 2              #caisson dia 
    Ac = math.pi * input_cache['D0']**2 / 4         #area caisson
    Mc = math.pi / 4 * (input_cache['D0']**2 - Di**2) * L * rhosteel #mass caison
    Mcb = math.pi / 4 * (input_cache['D0']**2 - Di**2) * L * rhowater #buoyancy
    Mce = Mc - Mcb #effective mass
    Wc = Mce * 9.81 #weight of caison
    Vc = 1
    V_comma = input_cache['V_LRP'] + Wc
    Ph = rhowater * 9.81 * input_cache['d']
    
    if input_cache['d'] > 50:
        SL = 5E5 #N/m**2, pump limit
    else:
        SL = Ph + 5E4 #N/m**2
        
    return {'L' : L, 'h':h, 'Di':Di, 'D':D, 'Ac':Ac,'Mc': Mc,'Mcb' : Mcb, 
            'Mce' : Mce, 'Wc':Wc,'V_comma' : V_comma, 'Ph':Ph, 'SL':SL}