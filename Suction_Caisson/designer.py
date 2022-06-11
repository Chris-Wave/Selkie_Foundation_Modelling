#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 10:10:03 2022

@author: goharshoukat

This is the Suction Caison foundation designer script

It makes use of the foundation_characterisitcs class

It defines the foundation dimensions and soil type. 

It will then determine if the caisson can penetrate the foundation under its
self-weight and if it can be set to its required depth wiothout violating the
limits imposed on the structure. 

The backend performs the necessary calculations to see if this design
will pass the necessary checks

It will then return an array with different diimensions which pass each of the
three tests. Further array manipulation will is then handled here which will then
provide the smallest dimensions which pass all three tests
"""

import numpy as np
import pandas as pd
from plot import plot
from Foundation_Characteristics import Foundation_Definition
from sklearn.preprocessing import MinMaxScaler
"""
The following properties must be defined in order to get the calculations going
d      : float : m, water depth
D0min  : float : m, outer diameter min
D0max  : float : m, outer diameter max
D0min  : float : m, outer diameter min
D0delta: float : m, outer diameter delta
Lmin   : float : m, skirt length min
Lmax   : float : m, skirt length max
Ldelta : float : m, skirt length delta
h_pert : float : m, height of caisson above seabed
t      : float : m, wall thickness
V_LRP  : float : N, vertical load reference point
V_ILRP : float : N, Vertical load under utility
H_LRP  : float : N, horizontal load reference point
M_LRP  : float : N, moment load reference point
Huls : float : N, horizontal loading from anchor
Vuls : float : N, Vertical loading from anchor
db     : float : m, chain diameter
The next set of inputs required will be stated when the specific portion of the
code is reached 
"""

#Values here are only assumed and might not present any realistic picture
d                   = 20
D0min               = 5
D0max               = 50
D0delta             = 1
Lmin                = 5
Lmax                = 50
Ldelta              = 1
h_pert              = .1
V_LRP               = 1e8
V_ILRP              = 1e5
H_LRP               = 1E4
M_LRP               = 1E4  #
Huls                = 1E4 
Vuls                = 1e1
db                  = 0.05 

#Iterations over an array of D0 are achieved through a for loop
#Vectorization for this will be achieved in the next iteration

D = np.arange(D0min, D0max, D0delta)
L = np.arange(Lmin, Lmax, Ldelta)
#declare dataframe to hold dimensions and their checks
dimensions = pd.DataFrame(columns={'D', 'L', 'M', 'Cost',
                                   'Self-weight installation',
                                   'Suction limit', 'Sliding',
                                   'Undrained bearing capacity', 
                                   'Drained bearing capacity',
                                   'Eccentricity'
                                   })

for i in D:
    for l in L:
    #declare FoundationA to be an instance of the class
    #if foundation type is an anchor, please specify Huls, Vuls and db. 
    #these are introduced as optional arguments and allow the code to 
    #perform regular calculations for just a simple foundation
    #provision of these will initiate the additional calculations for the 
    #anchor type foundation. 
        Foundation_A = Foundation_Definition(d, i, l, h_pert, V_LRP, V_ILRP, 
                                             H_LRP, M_LRP, Huls, Vuls, db)
        
        
# =============================================================================
#To be used when simple foundation is used.        
#  Foundation_A = Foundation_Definition(d, i, l, h_pert, V_LRP, V_ILRP, 
#                                              H_LRP, M_LRP)
#         
# =============================================================================
        """
        After class decleration, select soil type and soil subtype. For soil type, the 
        following options are available:
        1. Sand
        2. Clay
        
        The subtype for sand are:
        a. very loose
        b. loose
        c. medium dense
        d. dense
        e. very dense
        
        
        The subtype for clay are:
        a. extremely low strength
        b. very low strength
        c. low strength
        d. medium strength
        e. high strength
        f. very high strength
        
        Decleration of soil function does not return any value, however, it enables
        the next set of functions to perform their calculations and produce a cache
        of results
        
        Soil Properties are hard coded. They depend on the soil typoe and subtype 
        and the code will use those predefined properties. 
        
        
        """
        soil_type = 'sand'
        soil_subtype = 'dense'
        Foundation_A.soil_selection(soil_type, soil_subtype)
        
        
        """
        Finally, the smallest dimension that clears all checks are identified. 
        If in an nth iteration, no dimension which passes all three checks is obtained,
        nth + 1 iteration is performed. 
        
        The designe_check method is called and it returns the dimensions with their 
        checks. 
        """
        checker = Foundation_A.checker()
        frames = [checker, dimensions]
        dimensions = pd.concat(frames, join='inner', axis = 0, 
                               ignore_index=True, sort=False)
        
        #print('D = {}\nL = ')

#Plot the output


plot(dimensions, soil_type)
