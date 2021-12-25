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

    ex = ext_loads_dict['Mxuls'] / ext_loads_dict['Vv'] # unit (m)
    ey = ext_loads_dict['Myuls'] / ext_loads_dict['Vv'] # unit (m)
    Ix_min = max(6 * ex, geom) #might need tweaking
    Iy_min = max(6 * ey, geom)
    L_comma = max(Ix_min - 2 * ex, Iy_min - 2 * ey)
    B_comma = min(Ix_min - 2 * ex, Iy_min - 2 * ey)
    """
    After calculating L' and B', for iterations of multiple values, create
    a vector with a differential of at least 40 from the larger of the two valeus
    
    The vectorised approach towards multiplication, selection will help in avoiding
    unnecessary loops. 
    
    particular care was taken for the variable t which had severall selection
    steps. the min and max was done row by row without the use of any for loops 
    which was rigourously tested as well. 
    """
    if L_comma >= B_comma:
        end = L_comma + 40
    else:
        end = B_comma + 40

    L_vect = np.arange(L_comma, end, 0.5)
    B_vect = np.arange(B_comma, end, 0.5)
    A_comma = L_vect * B_vect #element wise multiplication of both vectors


    #row by row min max selection, eliminates the need for for loop
    t = np.max([0.3 * np.min([L_vect, B_vect], axis = 0), 
                np.ones(np.shape(A_comma))], axis = 0)
    v = A_comma * t
    W = v * 24
    Wb = W - v *10

    return pd.DataFrame({'L':L_vect, 'B':B_vect, 'A':A_comma, 't':t, 'v':v, 'W':W, 'Wb':Wb})