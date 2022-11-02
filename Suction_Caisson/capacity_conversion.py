#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 17:28:32 2021

@author: goharshoukat


This is the main library description for the suction caisson Foundation design for the 
Selkie Project

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 

Notes: Check with Chris what K is. 
"""
import math
import numpy as np
import logging
def capacity_conversions(input_cache, calc_cache, soil_type, soil_prop, K):
    #Input
    #input_cache: {}  : dictionary of user defined inputs 
    #soil_type  : str : string specifiying either clay or sand
    #calc_cache : {}  : dictionary from the precalc function
    #soil_prop  : {}  : dictionary with soil properties of the sub-type 
    #K          : float : to be checked with Chris
    #Output
    #cache : {} : dictionary with 3 important capacity conversion variables
    
    #clay undrained vertical capacity on outside of caisson
    if soil_type.lower() == 'clay':
        Vside = np.pi * calc_cache['D'] * calc_cache['h'] * \
                                        soil_prop['alpha'] * soil_prop['s_u']
        Hside = calc_cache['D'] * calc_cache['h'] * ((soil_prop['gamma'] * 
                                 calc_cache['h'] / 2) + ( 2* soil_prop['s_u'] ))
                                        
    
        Hbase = [calc_cache['D'] **2 *  np.pi / 4 * soil_prop['s_u']]
        #Vbase = input_cache['V_LRP'] + calc_cache['Wc'] - Vside
        hside = 2 * calc_cache['h'] /3 
        Mbase = (input_cache['M_LRP'] + hside * Hside + calc_cache['h'] * Hbase)
        H1 = input_cache['H_LRP'] - Hside
        logging.info('\n\n\n****Clay Capacity Conversions****')
        logging.info('\n Vside = {}\n Hside = {}\n Hbase = {}\n hside = {}\n Mbase = {}\n H1 = {}'.format(Vside, Hside, Hbase, hside, Mbase, H1))
    
# =============================================================================
#     
#   Code adaptation from dtocean for anchor based   
#     
#         
# =============================================================================

        if input_cache['L']/input_cache['D0'] <= 4.5:
            Nc = 6.2 * (1 + 0.34 * np.arctan(input_cache['L']/input_cache['D0']))
        else:
            Nc = 9
        logging.info('\nNc = {}'.format(Nc))
        As = np.pi * input_cache['D0'] * input_cache['L']
        Vu_dto = calc_cache['Ac'] * Nc * soil_prop['s_u'] + 0.65 * As + calc_cache['Wc'] 
        
        
        #lateral capacity, cohesive soils
        z = 0.7 * input_cache['L']
        Np = 3.6 / np.sqrt((0.75 - (z/input_cache['L']))**2 + (0.45 *(z/input_cache['L']))**2) #Changed "0.45 -" to "0.45 *"
        Hu_dto = input_cache['L'] * input_cache['D0'] * Np * soil_prop['s_u']
       
        
        Vbase = (input_cache['V_LRP'] + calc_cache['Wc']) - Vside
        logging.info('\n As = {}\n Vu_dto = {}\n z = {}\n  Np = {}\n Hu_dto = {}\n Vbase = {}'.format(
            As, Vu_dto, z, Np, Hu_dto, Vbase))
        return {'Vside' : Vside, 'Mbase' : Mbase,
                'H1' : H1, 'Hbase' : Hbase, 'Vu_dto' : Vu_dto,
                'Hu_dto' : Hu_dto,'Vbase' : Vbase}          
    
    
    #sand vertical capacity on outside of caisson
    elif soil_type.lower() == 'sand':
        logging.info('\n\n***Sand Capacity Conversion***')
        Vside = np.pi * calc_cache['D'] * calc_cache['h']**2 / 2 * K * \
                            soil_prop['gamma'] * math.tan(soil_prop['delta'])
        Kp = (1 + math.sin(soil_prop['phi'])) / (1 - math.sin(soil_prop['phi']))
        Ka = 1 / Kp
        Hside = soil_prop['gamma'] * calc_cache['h'] ** 2 * calc_cache['D'] \
            / 2 * (Kp - Ka)
        hside = 2 * calc_cache['h'] /3 
       
        #initial values for vbase. These will be overwritten and iterated through
        Vbase = (input_cache['V_LRP'] + calc_cache['Wc']) - Vside
        Hbase = Vbase * math.tan(soil_prop['phi'])
        Mbase = (input_cache['M_LRP'] + hside* Hside + calc_cache['h'] * Hbase)
        H1 = input_cache['H_LRP'] - Hside
        V1 = input_cache['V_LRP'] + calc_cache['Wc'] - Vside
        logging.info('Vside = {}\nKp = {}\nKa = {}\nHside = {}\nhside = {}\nVbase = {}\nHbase = {}\nMbase = {}\nH1 = {}\nV1 = {}'.format(
            Vside, Kp, Ka, Hside, hside, Vbase, Hbase, Mbase, H1, V1))
#the following calculations for capacity conversion are taken out of here and 
#into the bearing capacity checker for sand
#these are to be done iteratively with other vbase calculations                                
#        Hbase = input_cache['H_LRP'] - Hside
#        hside = 2 * calc_cache['h'] /3 
##        Vbase = input_cache['V_LRP'] + calc_cache['Wc'] - Vside
#        Mbase = (input_cache['M_LRP'] + hside * Hside + calc_cache['h'] * Hbase)
# =============================================================================

# =============================================================================
# 
# dtocean adaptation for anchor based  
# 
# =============================================================================
        K = 1 - np.sin(soil_prop['phi'])
        delta = 0.5 * soil_prop['phi']
        Vu_dto = calc_cache['Wc']+ np.pi / 2 * (input_cache['D0'] + calc_cache['Di']) * \
            input_cache['L'] ** 2 * soil_prop['gamma'] * K * np.tan(delta) #Corrected this 07/09/22 added division by 2 and (input_cache['D0'] + calc_cache['Di']) and added calc_cache['Wc']
        
        #lateral force
        #order changed to conform with our own equations. 
        # Removed this due to Stfans comments, only applicable to bearing caNq =  np.tan(math.radians(45) + (soil_prop['phi']/2))**2 * np.exp(np.pi * np.tan(soil_prop['phi']))
        # Hu_dto = 0.5 * input_cache['D0'] * Nq * soil_prop['gamma'] * input_cache['L']**2
        Hu_dto = Hside #Using same method as OWA
        logging.info('K = {}\ndelta = {}\nVu_dtop = {}\nHu_dto = {}'.format(
            K, delta, Vu_dto, Hu_dto))


        return {'Vside' : Vside, 'Ka' : Ka, 'Kp' : Kp, 'Mbase' : Mbase,
                 'Hbase' : Hbase, 'Vbase' : Vbase, 'hside' : hside,
                 'Hside' : Hside, 'H1' : H1, 'V1' : V1, 'Hu_dto' : Hu_dto, 
                 'Vu_dto' : Vu_dto}          


      