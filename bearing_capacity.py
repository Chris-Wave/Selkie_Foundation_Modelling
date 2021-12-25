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
from Eccentricity import eccent
def drained_bearing_capacity(phi, loads, c):
    #inputs
    #phi : float : degrees, obtained from the friction angle of soil
    #loads : {}dict : loads dictionary
    #c     : float : kPa, cohesion/safety factor
    phi = math.radians(phi) #convert degrees to radians for use in this function
    iq = 
    if phi == 0:
        Nq = 1
        Nc = 2 + math.pi
        Ngamma = 0
    else:
        Nq = math.exp(math.pi * math.tan(phi)) * \
                                    (math.tan(math.pi/4 + phi/2))**2
        Nc = (Nq - 1) / math.tan(phi)
        Ngamma = (Nq - 1) / math.tan(1.4 * phi)
        #Ngamma = 2 * (Nq + 1) * math.tan(phi) * math.tan(math.pi/4 + phi/5)
        
    
    
    
    
    
    
    kq = iq * sq
                            
                                    
    
        
    