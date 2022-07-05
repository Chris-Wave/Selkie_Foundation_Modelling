#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 15:17:04 2021

@author: goharshoukat

This function calculates the eccentricity and will be utilised using descriptors

This function feeds into the class foundation characteristics and soil_parameters

THis script is part of the Selkie Project

It is based off of Paul Bonar's adaptation of Majid Hussain's work. 

For details about the methodology, contact pbonar@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 

"""

import math
import numpy as np
import pandas as pd

def eccent(ext_loads_dict, geom):
    #ext_loads_dict : dictionary : user specified moments and forces
    #geom     : float : m, user-specified

    #output
    #returns a dictionary with all the calculations done, one data frame to
    #consolidate the vector calculations done starting with L_vect and then
    #everything before that is seperately cached in the dict. 
    
    #Calculate initial starting point for radius
    ex = ext_loads_dict['Mxuls'] / ext_loads_dict['Vv'] # unit (m)
    ey = ext_loads_dict['Myuls'] / ext_loads_dict['Vv'] # unit (m)
    Ix_min = max(6 * ex, geom) #might need tweaking
    Iy_min = max(6 * ey, geom)
    R=max(Ix_min,Iy_min)/2
    R_vect = np.linspace(R, R + 50, int(50/0.5))
    Be=2*np.min([R_vect-ex, R_vect-ey])
    Le=2*R*np.sqrt(1-(1-Be/(2*R_vect))**2)
    #L_comma = max(Ix_min - 2 * ex, Iy_min - 2 * ey) #AF note: Not quite DNV coded, but close
    #B_comma = min(Ix_min - 2 * ex, Iy_min - 2 * ey) #AF note: Not quite DNV coded, but close
    A_comma = 2*((R_vect**2)*np.cos(ex/R_vect)-ex*np.sqrt((R_vect**2))-(ex**2))
    #        A_comma currently only set up for x axis rotation.
    L_comma = np.sqrt(A_comma*Le/Be)
    B_comma = L_comma*Be/Le
    """
    After calculating L' and B', for iterations of multiple values, create
    a vector with a differential of at least 40 from the larger of the two values
    
    The vectorised approach towards multiplication, selection will help in avoiding
    unnecessary loops. 
    
    particular care was taken for the variable t which had severall selection
    steps. the min and max was done row by row without the use of any for loops 
    which was rigourously tested as well. 
    """
#    if L_comma >= B_comma:
#        steps = int((end - L_comma) / 0.5) 
#        end = L_comma + 50
#    else:
#        end = B_comma + 50
#        steps = int((end - B_comma) / 0.5)
#    L_vect = np.linspace(L_comma, end, steps)
#    B_vect = np.linspace(B_comma, end, steps)
#   #A_comma = L_vect * B_vect #element wise multiplication of both vectors


    #row by row min max selection, eliminates the need for for loop
    t = 0 #Thickness of embedment, AF made 0 manually.
    v = A_comma * t
    W = v * 24
    Wb = W - v * 10

    return {'Calc':pd.DataFrame({'L':L_comma, 'B':B_comma, 'A':A_comma, 'R' : R_vect, 't':t, 'v':v, 'W':W, 'Wb':Wb}),
         'ex':ex, 'ey':ey, 'Ix_min':Ix_min, 'Iy_min':Iy_min}


   
