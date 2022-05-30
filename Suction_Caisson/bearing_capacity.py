#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 16:32:11 2021

@author: goharshoukat

function untested, unintegrated. 
"""
import  math
import numpy as np
import matplotlib.pyplot as plt
def bearing_capacity(foundation_type, input_cache, calc_cache, soil_type, soil, cap_cache,
                     gamma_m, gamma_f):
    #Input
    #foundation_type     : str   : option for it to be 'anchor' or 'foundation'
    #input_cache: dict {} : dictionary of input cache
    #soil       : dict {} : dictionary of soil properties
    #calc_cache : dict {} : dictionary of pre calculations
    #cap_cache  : dict {} : dictionary of capacity cache
    #gamma_m    : float   : ahrd coded safety factor of material
    #gamma_f    : float   : hard coded favorable safety factor
 
    
    if soil_type == 'clay':
        if input_cache['M_LRP'] == 0:
            Aeff = math.pi * calc_cache['D']**2 / 4
            Beff = calc_cache['D']
            Leff = Beff
            ica = 0.5 - 0.5 * np.sqrt(1 - cap_cache['Hbase']/(
                Aeff * soil['s_u']))
            sca = 0.2 * ( 1 -2 * ica) * Beff/Leff
            dca = 0.3 * np.arctan(calc_cache['h'] / Beff)
            Vbase_R = Aeff * (soil['Nc'] * soil['s_u']*(1 + sca + dca - 
                                        ica) + soil['gamma'] * calc_cache['h'])
        elif input_cache['M_LRP'] > 0:
            #for i in range(len(cap_cache['Mbase'])):
            for i in range(len(cap_cache['Mbase'])):
            #iterate through vbase to get the actual vbase
                vbase =  cap_cache['Mbase'][i] / (calc_cache['D']/8)
                temp = 0
                Vbase_R = np.zeros(len(cap_cache['Mbase']))
                #plt.figure()
                
                for j in range(3):
                
                    e = cap_cache['Mbase'][i] / vbase
                    if e > calc_cache['D'] / 2:
                      #look at this later.   
                        raise Warning
                        print('Eccentricity greater than radius')
                        break
                        
                    
                    Aeff = 2*((calc_cache['D'] ** 2 / 4) * np.arccos(2 * e / calc_cache['D']) - e * 
                              np.sqrt((calc_cache['D']**2 / 4) - e**2))
  
                    Be = calc_cache['D'] - 2 * e

                    Le = np.sqrt(calc_cache['D']**2 - (calc_cache['D'] - Be)**2)
                    Leff = np.sqrt(Aeff * Le / Be)
                    Beff = np.sqrt(Aeff * Be/Le)
                    ica = 0.5 - 0.5 * np.sqrt(1 - cap_cache['Hbase'][i]/(
                        Aeff * soil['s_u']))
                    
                    sca = 0.2 * ( 1 -2 * ica) * Beff/Leff
                    dca = 0.3 * np.arctan(calc_cache['h'][i] / Beff)
                    vbase_r = Aeff * (soil['Nc'] * soil['s_u']*(1 + sca + dca - 
                                                ica) + soil['gamma'] * calc_cache['h'][i])
    
                    #plt.plot(range(i), Vbase_R[:i])
                    #plt.show()
                    
                    if abs(vbase_r - temp) < 1:
                        Vbase_R[i] = vbase_r
                        
    
                    else:
                        temp = vbase_r
                    

    #Perform bearing capacity check for undrained soil conditions
    #currently, incomplete data and equations are present
    #coding what we have access to for now. 
        undrained_bear_checker = (Vbase_R + cap_cache['Vside'])/gamma_m > (
        input_cache['V_LRP'] + calc_cache['Wc']) * gamma_f

    
        return {'undrained bearing capacity' : undrained_bear_checker}

    if soil_type=='sand' :     
    #Perform bearing capacity for drained sand
    #add the drained and undrained for sand. 
        for i in range(len(cap_cache['Mbase'])):
        #iterate through vbase to get the actual vbase
            vbase =  cap_cache['Mbase'][i] / (calc_cache['D']/8)
            temp = 0
            Vbase_R = np.zeros(len(cap_cache['Mbase']))
            #plt.figure()
            
            for j in range(10):
            
                e = cap_cache['Mbase'][i] / vbase
                if e > calc_cache['D'] / 2:
                  #look at this later.   
                    raise Warning
                    print('Eccentricity greater than radius')
                    break
                    
                
                Aeff = 2*((calc_cache['D'] ** 2 / 4) * np.arccos(2 * e / calc_cache['D']) - e * 
                          np.sqrt((calc_cache['D']**2 / 4) - e**2))
  
                Be = calc_cache['D'] - 2 * e

                Le = np.sqrt(calc_cache['D']**2 - (calc_cache['D'] - Be)**2)
                Leff = np.sqrt(Aeff * Le / Be)
                Beff = np.sqrt(Aeff * Be/Le)



                Bcomma = Beff
                Lcomma = Leff
        
                Nq = np.tan(math.pi / 4 + soil['phi'] / 2)**2 * np.exp(math.pi * 
                                                        math.tan(soil['phi']))
                Ngamma = 1.5 * (Nq - 1) * math.tan(soil['phi'])    
                iq = 1 - 0.5 * (cap_cache['Hbase'][i] / vbase)**5
                sq = 1 + iq * (Bcomma / Lcomma) * math.sin(soil['phi'])
                igamma = 1 - 0.7 * (cap_cache['Hbase'][i] / vbase)**5
                sgamma = 1 - 0.4 * igamma * Bcomma / Lcomma
                dq = 1+ 1.2 * calc_cache['h'][i]/Bcomma * math.tan(soil['phi']) * (1 - 
                                                        math.sin(soil['phi']))**2
                dgamma = 1
                vbase_r = Aeff * (0.5 * soil['gamma'] * Beff * Ngamma * sgamma * dgamma * 
                          igamma + soil['gamma'] * calc_cache['h'][i] * Nq * sq * 
                          dq * iq)
        
                if abs(vbase_r - temp) < 1:
                    Vbase_R[i] = vbase_r
                    
        
                else:
                    temp = vbase_r
                
        drained_bear_checker = (Vbase_R + cap_cache['Vside'])/gamma_m > (
        input_cache['V_LRP'] + calc_cache['Wc']) * gamma_f

        #for i in range(len(cap_cache['Mbase'])):
        for i in range(len(cap_cache['Mbase'])):
        #iterate through vbase to get the actual vbase
            vbase =  cap_cache['Mbase'][i] / (calc_cache['D']/8)
            temp = 0
            Vbase_R = np.zeros(len(cap_cache['Mbase']))
            #plt.figure()
            
            for j in range(10):
            
                e = cap_cache['Mbase'][i] / vbase
                if e > calc_cache['D'] / 2:
                  #look at this later.   
                    raise Warning
                    print('Eccentricity greater than radius')
                    break
                    
                
                Aeff = 2*((calc_cache['D'] ** 2 / 4) * np.arccos(2 * e / calc_cache['D']) - e * 
                          np.sqrt((calc_cache['D']**2 / 4) - e**2))
  
                Be = calc_cache['D'] - 2 * e

                Le = np.sqrt(calc_cache['D']**2 - (calc_cache['D'] - Be)**2)
                Leff = np.sqrt(Aeff * Le / Be)
                Beff = np.sqrt(Aeff * Be/Le)
                ica = 0.5 - 0.5 * np.sqrt(1 - (cap_cache['Hbase'][i]/(
                    Aeff * soil['s_u'])))
                
                sca = 0.2 * ( 1 -2 * ica) * Beff/Leff
                dca = 0.3 * np.arctan(calc_cache['h'][i] / Beff)
                vbase_r = Aeff * (soil['Nc'] * soil['s_u']*(1 + sca + dca - 
                                            ica) + soil['gamma'] * calc_cache['h'][i])

                #plt.plot(range(i), Vbase_R[:i])
                #plt.show()
                
                if abs(vbase_r - temp) < 1:
                    Vbase_R[i] = vbase_r
                    

                else:
                    temp = vbase_r
                

#Perform bearing capacity check for undrained soil conditions
#currently, incomplete data and equations are present
#coding what we have access to for now. 
        undrained_bear_checker = (Vbase_R + cap_cache['Vside'])/gamma_m > (
    input_cache['V_LRP'] + calc_cache['Wc']) * gamma_f

# =============================================================================
#         return {'drained bearing capacity' : drained_bear_checker,
#                 'undrained bearing capacity' : undrained_bear_checker}
# 
# 
# =============================================================================
        return {'drained bearing capacity' : drained_bear_checker}

