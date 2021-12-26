#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 23:54:46 2021

@author: goharshoukat

This function calculates the bearing capacity and will be utilised using descriptors
This file links into the class soil_parameters

it has two parts: 
    drained
    undrained
both will be covered in this script and will be bounded to the class via descriptors

THis script is part of the Selkie Project

It is based off of Paul Bonar's adaptation of Majid Hussain's work. 

The drained analysis makes use of the Meyerhof's methodology'
For details about the methodology, contact pbonar@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 

"""
import math
import numpy as np
from Eccentricity import eccent
def bearing_capacity(phi, loads, c, geom, weight, Df, Hs, SF, embed=False):
    #inputs
    #phi : float : degrees, obtained from the friction angle of soil
    #loads : {}dict : loads dictionary, passed on from function file external_loads
    #c     : float : kPa, cohesion/safety factor
    #geom  : float : m, passed on because eccent function needs this
    #weight : float : kN/m3, weight of soil
    #Df     : float : m, depth of foundation
    #Hs     : float : m, Side soil contact
    #SF     : float : safety factor for bearing capacity
    #embed : bool : True if there is an embediment, false otherwise
    
    
    #output
    #Qu_SF : pd.Series : bearing capacity adjusted for safety for 
    #several dimensions. 
    phi = math.radians(phi) #convert degrees to radians for use in this function
    
    """
    vectorised approach wil be taken to compute iq, ic, m since in the input
    parameters l' and b' are both vectors
    """
    cache = eccent(loads, geom)
    iq = (1 - (loads['Vh']/(loads['Vv'] + cache['Ix_min'] * cache['Iy_min'] * 
                            c / math.tan(phi))))**2
    theta = 0
    m = ((2 + cache['Ix_min']/cache['Iy_min']) / (1 + \
        cache['Ix_min']/cache['Iy_min'])) * math.cos(theta)**2 + \
        ((2 + cache['Iy_min'] / cache['Ix_min']) / (1 + \
        cache['Iy_min']/cache['Ix_min'])) * math.sin(theta)**2
    
    if phi == 0:
        
        Nq = 1
        Nc = 2 + math.pi
        Ngamma = 0
        theta = 0
        ic = 1 - (m * loads['Vh']/(cache['Ix_min'] * cache['Iy_min'] * c * Nc))    
    
    else:
        Nq = math.exp(math.pi * math.tan(phi)) * \
                                    (math.tan(math.pi/4 + phi/2))**2
        Nc = (Nq - 1) / math.tan(phi)
        Ngamma = (Nq - 1) / math.tan(1.4 * phi)
        #Ngamma = 2 * (Nq + 1) * math.tan(phi) * math.tan(math.pi/4 + phi/5)
        ic = iq - (1 - iq)/(Nc * math.tan(phi))

    sq = 1 + cache['Calc'].B / cache['Calc'].L *math.tan(phi)  
    sc = 1 + geom / cache['Ix_min'] * Nq/Nc 
    kc = ic * m   
    igamma = (1 - loads['Vh']/(loads['Vv'] + cache['Ix_min'] * cache['Iy_min'] * \
                              c / math.tan(phi) )) ** 4
    sgamma = 1 - 0.4*cache['Iy_min']/cache['Ix_min']
    kgamma = sgamma * igamma
    qc = c * Nc * kc
    kq = iq * sq
    
    if embed:
        qq = weight * Hs * ( 1 + Nq * kq - 1)
    else:
        qq = 0
    
    qgamma = weight * cache['Iy_min']/2 * Ngamma * kgamma
    RHS = 2 * (cache['Calc'].L + cache['Calc'].B) * Hs * (c + weight * 0.5 *
            (Df + np.max([np.zeros(len(cache['Calc'].t)), Df - cache['Calc'].t -
                         Hs], axis = 0))) * math.tan(phi - 5)
    Qu = cache['Calc'].A * (qc + qq + qgamma) + RHS
    Qu_SF = Qu/SF
    
    return Qu_SF


                            
"""                                    
m  = bearing_capacity(3, loads, 10, 5, 10, 10, 10, 8)    
checker = m > 10000        
z = cache2['Calc'][checker].reset_index(drop = True)
z = z[checker].reset_index(drop=True).iloc[0]
z.iloc[0]
#rhs =(1 + np.max([np.zeros((len(cache2['Calc'].t))), cache2['Calc'].t-5], axis = 0)) 
"""