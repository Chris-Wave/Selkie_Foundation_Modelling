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
import logging


def bearing_capacity(input_cache, calc_cache, soil_type, soil, cap_cache,
                     gamma_m, gamma_f):
    #Input
    #input_cache: dict {} : dictionary of input cache
    #soil       : dict {} : dictionary of soil properties
    #calc_cache : dict {} : dictionary of pre calculations
    #cap_cache  : dict {} : dictionary of capacity cache
    #gamma_m    : float   : ahrd coded safety factor of material
    #gamma_f    : float   : hard coded favorable safety factor
 
    
    if soil_type == 'clay':
        # if input_cache['M_LRP'] == 0:
        #     Aeff = math.pi * calc_cache['D']**2 / 4
        #     Beff = calc_cache['D']
        #     Leff = Beff
        #     ica = 0.5 - 0.5 * np.sqrt(1 - cap_cache['H1']/(
        #         Aeff * soil['s_u']))
        #     sca = 0.2 * ( 1 -2 * ica) * Beff/Leff
        #     dca = 0.3 * np.arctan(calc_cache['h'] / Beff)
        #     Vbase_R = Aeff * (soil['Nc'] * soil['s_u']*(1 + sca + dca - 
        #                                 ica) + soil['gamma'] * calc_cache['h'])
        #     undrained_bear_checker = (Vbase_R + cap_cache['Vside'])/gamma_m > (
        #                     input_cache['V_LRP'] + calc_cache['Wc']) * gamma_f

        #     return {'undrained bearing capacity' : undrained_bear_checker}
        
        # elif input_cache['M_LRP'] > 0:
            for i in range(len(cap_cache['Mbase'])):
                #th following method is not matrix friendly. 
                #for matrix multiplication a few changes will have to be made
                #esp the eccentricity checks will need special catering 
                
                logging.info('****\n\n\nClay Bearing Capacity Check****')
                logging.info('\nSubiteration 0')
                
                vbase = cap_cache['Mbase'][i] / (calc_cache['D']/8)
                temp = 0 #dummy variable to hold the previous iteration value
                Vbase_R = np.zeros(len(cap_cache['Mbase'])) #vector to hold all the vbase values to perform the check; #this will have to come out of the loop when vectorization is implemented. 
                Vbase_R[i] = vbase
                #doesnt matter right now. 
                
                
                #check for eccentricicty. break the loop and return a failed check for this particular set of dimensions
                e = cap_cache['Mbase'][i] / cap_cache['Vbase'] 
                logging.info('\nvbase = {}\nVbase_R[i] = {}\ne = {}'.format(vbase, Vbase_R[i], e))
                
                j = 0
                error = 999         
                #run iterations for convergence of vbase
                while error > 1:
                    j+=1
                    logging.info('\nSubiteration {}'.format(j+1))
                    #print('j=',j)
                    if e < 0 :
                        Aeff = math.pi * calc_cache['D']**2 / 4
                        Beff = calc_cache['D']
                        Leff = Beff
                        ica = 0.5 - 0.5 * np.sqrt(1 - cap_cache['H1']/(Aeff * soil['s_u']))
                        sca = 0.2 * ( 1 -2 * ica) * Beff/Leff
                        dca = 0.3 * np.arctan(calc_cache['h'] / Beff)
                        Vbase_R = Aeff * (soil['Nc'] * soil['s_u']*(1 + sca + dca - 
                                             ica) + soil['gamma'] * calc_cache['h'])
                        undrained_bear_checker = (Vbase_R + cap_cache['Vside'])/gamma_m > (
                                 input_cache['V_LRP'] + calc_cache['Wc']) * gamma_f
                        
                        logging.info('\nAeff = {} \nBeff = {}\nLeff = {}\nica = {}\nsca = {}\ndca = {}\nVbase_R= {}\nundrained_bear_checker= {}'.format(Aeff, Beff, Leff,ica,sca,dca,Vbase_R,undrained_bear_checker))
                        
                        return {'undrained bearing capacity' : undrained_bear_checker}    
                
                    elif e > calc_cache['D'] / 2 :
                        
                    
                        undrained_bear_checker = False
                        logging.info('\ne = {} \nundrained_bear_checker'.format(e,undrained_bear_checker))
                        #print(undrained_bear_checker)
                        return {'undrained bearing capacity' : undrained_bear_checker}
                    
                    else:
                        Aeff = 2*((calc_cache['D'] ** 2 / 4) * np.arccos((2 * e) / calc_cache['D']) - (e * 
                                  np.sqrt((calc_cache['D']**2 / 4) - e**2)))
                        
                        Be = calc_cache['D'] - 2 * e
                        Le = np.sqrt(calc_cache['D']**2 - (calc_cache['D'] - Be)**2)
                        Leff = np.sqrt(Aeff * (Le / Be))
                        Beff = np.sqrt(Aeff * (Be/Le))
                        
                        if cap_cache['H1'][i]/(Aeff * soil['s_u'])>1:
                            #undrained_bear_checker = False
                            #return {'undrained bearing capacity' : undrained_bear_checker}
                            ica = 0.5
                        else:
                            if input_cache['H_LRP'] == 0:
                                ica = 0
                            else:
                                ica = 0.5 - 0.5 * np.sqrt(1 - cap_cache['H1'][i]/(
                                Aeff * soil['s_u']))
                            
                            
                        sca = 0.2 * ( 1 -2 * ica) * Beff/Leff
                        dca = 0.3 * np.arctan(calc_cache['h'][i] / Beff)
                        vbase_r = Aeff * (soil['Nc'] * soil['s_u']*(1 + sca + dca - 
                                                    ica) + soil['gamma'] * calc_cache['h'][i])
                        
                        error = abs(vbase_r - temp) 
                        logging.info('\nAeff = {} \nBeff = {}\nLeff = {}\nica = {}\nsca = {}\ndca = {}\nVbase_R= {}'.format(Aeff, Beff, Leff,ica,sca,dca,Vbase_R))
                            
                       
                        temp = vbase_r
                        e = cap_cache['Mbase'][i] / vbase_r #added this back in as couldnt see why it was removed #removed as eccentricity wont change
                        Vbase_R[i] = vbase_r
                            #print('e=',e)
                        #this statement has to be outside the for loop
                        #‘hence the check has to be reimposed. 
                        #the several loops are making the code untidy
                        #once  vectorization implemented, code can 
                        #be cleaner
                        logging.info('\nerror = {}\nVbase_R[i] = {}\ne = {}'.format(error, Vbase_R[i], e))
                
                    undrained_bear_checker = (Vbase_R + cap_cache['Vside'])/gamma_m > (
                            input_cache['V_LRP'] + calc_cache['Wc']) * gamma_f
                   # print(undrained_bear_checker)
                        
                    return {'undrained bearing capacity' : undrained_bear_checker}
                    logging.info('\nAfter final subiteration:\nundrained bearing capacity = {} '.format(undrained_bear_checker))
                             
                
    if soil_type=='sand' :     

        for i in range(len(calc_cache['h'])):
            #th following method is not matrix friendly. 
            #for matrix multiplication a few changes will have to be made
            #esp the eccentricity checks will need special catering 
      
        #this will have to come out of the loop when vectorization is implemented. 
        #doesnt matter right now. 
            Vbase_R = np.zeros(len(cap_cache['Mbase'])) #vector to hold all the vbase values to perform the check
            Vbase_R[i] = cap_cache['Vbase'] #if value is not updated, Vbase_R will have the initialized value at least for the final check, otherwise iteration will not produce any results        
            
            #check for eccentricicty. break the loop and return a failed check for this particular set of dimensions
            
            e = cap_cache['Mbase'][i] / cap_cache['Vbase'] 
            #e = calc_cache['D'] / 8 #
            
            logging.info('****\n\n\nSand Bearing Capacity Check****')
            logging.info('\nSubiteration 0')
            logging.info('\nVbase_R[i] = {}\ne = {}'.format(Vbase_R[i], e))
                
            
            
            if e > calc_cache['D'] / 2 :
                drained_bear_checker = False
                logging.info('\ne > calc_cache[D] / 2 = {}'.format(drained_bear_checker))
                
                break
            
            else:                    
                #run iterations for convergence of vbase
                #create more variables which will hold the initialized values
                #these values will get updated at the end of the loop
                Hbase = cap_cache['Hbase'][i]
                vbase = cap_cache['Vbase'][i]
                Mbase = cap_cache['Mbase'][i]
                V1 = cap_cache['V1'][i]
                H1 = cap_cache['H1'][i]
                temp = vbase    #dummy variable to hold the previous iteration value
                j = 0
                error = 999  
                while error > 1: #removed previous version of this loop, that ran three times irregarless of convergence OLD version:#3 iterations for now
                    j+=1
                    logging.info('\nSubiteration {}'.format(j))
                    if e > calc_cache['D'] / 2 :
                        drained_bear_checker = False
                        return {'drained bearing capacity' : drained_bear_checker}
                        
                    Aeff = 2*((calc_cache['D'] ** 2 / 4) * np.arccos((2 * e) / calc_cache['D']) - (e * 
                              np.sqrt((calc_cache['D']**2 / 4) - e**2)))
                    
                    Be = calc_cache['D'] - 2 * e
                    Le = np.sqrt(calc_cache['D']**2 - (calc_cache['D'] - Be)**2)
                    Leff = np.sqrt(Aeff * (Le / Be))
                    Beff = np.sqrt(Aeff * Be/Le)
        
                    Bcomma = Beff
                    Lcomma = Leff
                    
        
                    Nq = np.tan(math.pi / 4 + soil['phi'] / 2)**2 * np.exp(math.pi * 
                                                            math.tan(soil['phi']))
                    Ngamma = 1.5 * (Nq - 1) * math.tan(soil['phi'])    
                    #iq = (1 - 0.5 * (H1 / (V1 + Aeff * soil['Nc'] * (1/np.tan(soil['phi'])))))**5
                    
                    #iq and igamma blow up which fails the bearing check
                    #if h1 or v1 are negative, its a load inclination factor and not a capacity inclination 
                    #factor, it becomes irrelevant. 
                    if (H1 < 0) or (V1 < 0):
                        iq, igamma = 1, 1

                    elif H1 > V1:
                        return {'drained bearing capacity' : False}                        
                    
                    else:
                        iq = (1 - 0.5 * (H1 / (V1)))**5
                        igamma = (1 - 0.7 * (H1 / (V1)))**5
                        
                    sq = 1 + iq * (Bcomma / Lcomma) * math.sin(soil['phi'])
                    #igamma = (1 - 0.7 * (H1 / (V1 + Aeff * soil['Nc'] * (1/np.tan(soil['phi'])))))**5

                    
                    sgamma = 1 - (0.4 * igamma * (Bcomma / Lcomma))
                    dq = 1+ 1.2 * (calc_cache['h'][i]/Bcomma) * math.tan(soil['phi']) * (1 - 
                                                            math.sin(soil['phi']))**2
                    dgamma = 1
                    vbase_r = Aeff * (0.5 * soil['gamma'] * Beff * Ngamma * sgamma * dgamma * 
                              igamma + soil['gamma'] * calc_cache['h'][i] * Nq * sq * 
                              dq * iq)
        
                    if abs(vbase_r - temp) < 1:
                        Vbase_R[i] = vbase_r
                        
            
                    else:
                        temp = vbase_r
                        #update Hbase, Mbase with the new value
                        vbase = vbase_r
                        Hbase = vbase * math.tan(soil['phi'])
                        Mbase = (input_cache['M_LRP'] + cap_cache['Hside'] * cap_cache['hside'] + calc_cache['h'] * Hbase)
                        e = Mbase/vbase
                        x = 1

                    error = abs(vbase_r - temp) 
                    logging.info('\nAeff = {} \nBeff = {}\nLeff = {}\nNq = {}\nNgamma = {}\niq = {}\nigamma = {}\nsq = {}\nsgamma = {}\ndq = {}\ndgamma = {}\nVbase_R= {}\nHbase= {}\nMbase= {}\ne= {}'.format(Aeff, Beff, Leff,Nq, Ngamma,iq,igamma,sq,sgamma,dq,dgamma,Vbase_R,Hbase,Mbase,e))
                        
            drained_bear_checker = (Vbase_R + cap_cache['Vside'])/gamma_m > (
                input_cache['V_LRP'] + calc_cache['Wc']) * gamma_f

            logging.info('\nAfter final subiteration:\nAeff = {} \nBeff = {}\nLeff = {}\nNq = {}\nNgamma = {}\niq = {}\nigamma = {}\nsq = {}\nsgamma = {}\ndq = {}\ndgamma = {}\nVbase_R= {}\nHbase= {}\nMbase= {}\ne= {}\ndrained_bear_checker= {}'.format(Aeff, Beff, Leff,Nq, Ngamma,iq,igamma,sq,sgamma,dq,dgamma,Vbase_R,Hbase,Mbase,e,drained_bear_checker))
                     

# =============================================================================
#         return {'drained bearing capacity' : drained_bear_checker,
#                 'undrained bearing capacity' : undrained_bear_checker}
# 
# 
# =============================================================================
        return {'drained bearing capacity' : drained_bear_checker}

