#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 23:54:46 2021

@author: goharshoukat

This function calculates the bearing capacity and will be utilised using descriptors
This file links into the class foundation_characteristics

it has two parts: 
    drained
    undrained
both will be covered in this script and will be bounded to the class via descriptors

This script is part of the Selkie Project

It is based off of Paul Bonar's adaptation of Majid Hussain's work. 

The drained analysis makes use of the Meyerhof's methodology'
For details about the methodology, contact pbonar@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 

"""
import math
import numpy as np
from Eccentricity import eccent
def bearing_capacity(phi, loads, load_check, c, geom, weight, Df, Hs, 
                     sensitivity, SF,  embed=False):
    #inputs
    #phi : float : degrees, obtained from the friction angle of soil
    #loads : {}dict : loads dictionary, passed on from function file external_loads
    #load_check : pd.series : single value per dimension used for capacity check
    #c     : float : kPa, cohesion/safety factor
    #geom  : float : m, passed on because eccent function needs this
    #weight : float : kN/m3, weight of soil
    #Df     : float : m, depth of foundation
    #Hs     : float : m, Side soil contact
    #sensitivity : float : user defined sensitivity parameter
    #SF     : float : safety factor for bearing capacity
    #embed : bool : True if there is an embediment, false otherwise
    
    
    #output
    #checker_bearingcap : pd.Series : series of booleans for dims that pass the 
    #design check necessary for bearing_cap
    phi = math.radians(phi) #convert degrees to radians for use in this function
    
    """
    vectorised approach wil be taken to compute iq, ic, m since in the input
    parameters l' and b' are both vectors
    """
    cache = eccent(loads, geom)
    
    # theta = 0
    # m = ((2 + cache['Ix_min']/cache['Iy_min']) / (1 + \
    #     cache['Ix_min']/cache['Iy_min'])) * math.cos(theta)**2 + \
    #     ((2 + cache['Iy_min'] / cache['Ix_min']) / (1 + \
    #     cache['Iy_min']/cache['Ix_min'])) * math.sin(theta)**2
    
    if phi == 0: #Undrained calculation according to DNVGL-RP-C212 Section 5.4.7.1
        
        #Nq = 1
        Nc = 2 + math.pi
        #Ngamma = 0
        #theta = 0
        Rho = ((cache['R']**2)*math.pi()-cache['Calc'].A)*c #sliding resistance on horizontal area outside effective area [kPa]\n",
        Rhp = 0 #No embedded members
        H1 = loads['Vh']-Rho-Rhp
        ica = 0.5 - 0.5*math.sqrt(1-H1/(cache['Calc'].A*c))
        sca = 0.2*(1-2*ica)*cache['Calc'].B/cache['Calc'].L
        dca=0 #No embedment, D=0, atan(0)=0
        p0=0 #No embedment.
        qc = c * Nc * (1+sca+dca-ica)+p0  
  #      ic = 1 - (m * loads['Vh']/(cache['Ix_min'] * cache['Iy_min'] * c * Nc))
    
    else: #Drained calculation
        iq = (1 - (0.5*loads['Vh']/(loads['Vv'] + cache['Calc'].A * 
                                c / math.tan(phi))))**5
        
        igamma = (1 - (0.7*loads['Vh']/(loads['Vv'] + cache['Calc'].A * 
                                c / math.tan(phi))))**5
        Nq = math.exp(math.pi * math.tan(phi)) *(math.tan(math.pi/4 + phi/2))**2
        #Nc = 2 + math.pi
   #     Ngamma_1 = (Nq - 1) / math.tan(1.4 * phi)
        Ngamma_2 = 2 * (Nq + 1) * math.tan(phi)
        Ngamma = np.min([Ngamma_2], axis = 0)
        #ic = iq - (1 - iq)/(Nc * math.tan(phi))
        

    sq = 1 + iq*cache['Calc'].B / cache['Calc'].L *math.sin(phi)  
   # sc = 1 + geom / cache['Ix_min'] * Nq/Nc 
   # kc = ic * m   
  #  igamma = (1 - loads['Vh']/(loads['Vv'] + cache['Ix_min'] * cache['Iy_min'] * \
   #                           c / math.tan(phi) )) ** 4
    sgamma = 1 - 0.4*igamma*cache['Calc'].B/cache['Calc'].L 
  #  kgamma = sgamma * igamma
    
    #kq = iq * sq
    
    a=c/math.tan(phi)
    p0=0 #For no embedment.
    dgamma=1
    dq=1+1.2*Hs/cache['Calc'].B * math.tan(phi)*((1-math.sin(phi))**2)
    qc = 0.5 * cache['Calc'].B *sgamma *Ngamma *igamma*dgamma*(weight-10)+(p0+a)*Nq*sq*dq*iq-a 
    #qc assumes water density =10kN/m3
    if embed:
        qq = 0 #AF artifically made this 0 to be sure not included.
    else:
        qq = 0
    
    #qgamma = weight * cache['Iy_min']/2 * Ngamma 
    #RHS = 2 * (cache['Calc'].L + cache['Calc'].B) * Hs * (c/sensitivity + 
    #      weight * 0.5 * (Df + np.max([np.zeros(len(cache['Calc'].t)), Df - 
    #   cache['Calc'].t - Hs], axis = 0))) * math.tan(phi - 5)
    Qu = cache['Calc'].A * (qc)
    Qu_SF = Qu/SF
    
    checker_bearingcap = Qu_SF > load_check # see from the entire stack of
    #dataframe with different dimensions, which pass the test
    #select the one with the smallest dimensions. 
    


    return checker_bearingcap


                            
"""                                    
m  = bearing_capacity(3, loads, 10, 5, 10, 10, 10, 8)    
checker = m > 10000        
z = cache2['Calc'][checker].reset_index(drop = True)
z = z[checker].reset_index(drop=True).iloc[0]
z.iloc[0]
#rhs =(1 + np.max([np.zeros((len(cache2['Calc'].t))), cache2['Calc'].t-5], axis = 0)) 
"""