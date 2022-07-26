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
import warnings
warnings.filterwarnings("ignore")
def precalculations(input_cache, soil_type, soil_prop, rhosteel, rhowater, 
                    mooring_cache : False):
    #input
    #input_cache : {} dict : dict of floats with user inputs as cache 
    #soil_type : str : sand or clay
    #soil_prop : dict : cache of soil type
    #rhosteel : float : kg/m**3, density of steel
    #rhowater : flat : kg/m**3, water density
    #mooring_cache : {} dict : dictionary of mooring forces
    #output
     #cache : dict: dictionary with results of all the below calculations
    
    #L = np.arange(input_cache['Lmin'],input_cache['Lmax'], input_cache['Ldelta'])
    L = input_cache['L']
    L = np.arange(L, L+1, 1)

    h = L - input_cache['h_pert']               #installed depth
    Di = input_cache['D0'] - 2 * input_cache['t']                #inner dia
    D = (Di + input_cache['D0']) / 2              #caisson dia 
    Ac = math.pi * input_cache['D0']**2 / 4         #area caisson
    mass_skirt = math.pi * D * input_cache['t'] * L *rhosteel
    mass_top_plate = 1/4 * math.pi * (D**2) * (2 * input_cache['t']) * rhosteel
    #Mc = math.pi / 4 * (input_cache['D0']**2 - Di**2) * L * rhosteel #mass caison
    Mc = mass_skirt + mass_top_plate
    
    #Mcb will exist but will not be used. 
    #Mcb = math.pi / 4 * (input_cache['D0']**2 - Di**2) * L * rhowater #buoyancy
    
    Mce = Mc * (rhosteel - rhowater)/rhosteel  # - Mcb #effective mass
    Wc = Mce * 9.81 #weight of caison
    #V_comma = input_cache['V_LRP'] + Wc
    V_comma = (input_cache['V_LRP'] + Wc)
    V_comma_install = (input_cache['V_ILRP'] + Wc)
    Ph = rhowater * 9.81 * (input_cache['d'] - input_cache['h_pert'])
    
    if input_cache['d'] > 50:
        SL = 5E5 #N/m**2, pump limit
    else:
        SL = Ph + 5E4 #N/m**2
    
    
    
# =============================================================================
# 
#     Precalculations for the Anchor based tool
#     Will be executed if mooring cache exists
#     otherwise entire block will be skipped
# =============================================================================
    if mooring_cache['Huls']:
        za = input_cache['L'] * 0.7
        
        #removed 1.8 SF from here, the user will be recommedned to include the SF in their input forces.
        Tm = np.sqrt(mooring_cache['Huls']**2 + mooring_cache['Vuls']**2)
        
        theta_m = np.arctan(mooring_cache['Vuls'] / mooring_cache['Huls'])
        
        if soil_type.lower() == 'clay':
            mu = 0.4 #value is adopted directly
        
            #Ta needs to be iterated through. initial guess = 0
            #if mooring loads are too low, all the force is taken by the soil
            #none of the force makes it to the anchor. 
            #theta_a and Ta become infitity and zero respecitivley
            #therefore check should pass
            #Ta calculations wil then be bypassed to prevent an error
            #alternatively warning message can be supressed. 
            
            theta_a = theta_m * 2
            dummy = 0
            Ta = Tm
            for i in range(10):
                Q = 2.5 * mooring_cache['db'] * 11.5 * soil_prop['s_u']
                
                #if the solution blows up, assign values and exit the loop
                #eccentrity checks will recognize the nan, inf and 0 as a sign of divergence and the check will pass
                if np.exp(mu * (theta_a - theta_m)) ==float('inf'):
                    Ta = 0
                    theta_a = float('inf')
                    break
                else:
                    Ta = Tm / (np.exp(mu * (theta_a - theta_m)))
                    theta_a = np.sqrt(theta_m**2 + ((2 * Q * za )/Ta))
                
                if abs(dummy - theta_a) < 0.01:
                    break
                else:
                    dummy = theta_a                
        elif soil_type.lower() =='sand':
            #Ta needs iteration
            mu = 0.4 #value taken frmo clay. different for sand but dont have it right now. 
            Nq =  np.tan(math.radians(45) + (soil_prop['phi']/2))**2 * np.exp(np.pi * np.tan(soil_prop['phi']))
            theta_a = theta_m * 2
            dummy = 0
            Ta = Tm
            for i in range(10):
                Q = 2.5 * mooring_cache['db'] * Nq * soil_prop['gamma'] * za
                
                #if the solution blows up, assign values and exit the loop
                #eccentrity checks will recognize the nan, inf and 0 as a sign of divergence and the check will pass
                if np.exp(mu * (theta_a - theta_m)) ==float('inf'):
                    Ta = 0
                    theta_a = float('inf')
                    break
                else:
                    Ta = Tm / (np.exp(mu * (theta_a - theta_m)))
                    theta_a = np.sqrt(theta_m**2 + ((2 * Q * za )/Ta))
                
                if abs(dummy - theta_a) < 0.01:
                    break
                else:
                    dummy = theta_a         
        
        return {'L' : L, 'h':h, 'Di':Di, 'D':D, 'Ac':Ac,'Mc': Mc,# 
                'Mce' : Mce, 'Wc':Wc,'V_comma' : V_comma, 'Ph':Ph, 'SL':SL,
                'V_comma_install' : V_comma_install, 'Ta' : Ta, 'theta_a' : theta_a}
    
    else:#if no mooring_cache, return items will not contain mooring calcs. 
        return {'L' : L, 'h':h, 'Di':Di, 'D':D, 'Ac':Ac,'Mc': Mc,# 
                'Mce' : Mce, 'Wc':Wc,'V_comma' : V_comma, 'Ph':Ph, 'SL':SL,
                'V_comma_install' : V_comma_install}
    
    