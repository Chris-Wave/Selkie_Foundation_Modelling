#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:08:33 2021

@author: goharshoukat

Foundation properties and material characteristics are defined in this class. 

This is the main library description for the suction caisson Foundation design for the 
Selkie Project

Note: The module accepts a singular value of D0. Iterations over several 
values of D0 is achieved in the designer script - outside of this module. 
Improvements to this will be made in the next revisions

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""


import math
import pandas as pd
from precalculation import precalculations
from soil_properties import soil    
from capacity_conversion import capacity_conversions as cc #to avoid naming conflicts as the name of a method is also capacity conversion
from installation import installation_sand, installation_clay
from bearing_capacity import bearing_capacity
from sliding import sliding
from uplift import uplift

class Foundation_Definition:
    #these properties can be changed for the class instance if needed
    
    gravity     = 9.81
    K           = 0.5
    v           = 0.3 #poisson ratio
    rhosteel    = 8050 
    E           = 210E6    #young's modulus
    rhowater    = 1025 #density of water
    gamma_m     = 1.15 #safety factor of material
    gamma_f     = 0.9 #favorable safety factor load factor
    gamma_uf    = 1.1 #unfavorable safety factor load
    
    
    def __init__(self, d, D0, L, Lmin, Lmax, Ldelta, h_pert, t, 
                 V_LRP, H_LRP, M_LRP):
        #inputs
        #d      : float : m, water depth
        #D0     : float : m. outer diameter
        #L      : float : m, skirt length
        #Lmin   : float : m, skirt length min
        #Lmax   : float : m, skirt length max
        #Ldelta : float : m, skirt length delta
        #h_pert : float : m, height of caisson above seabed
        #t      : float : m, wall thickness
        #V_LRP  : float : m, vertical load reference point
        #H_LRP  : float : m, horizontal load reference point
        #M_LRP  : float : m, moment load reference point
        t = .02 * D0           #assumed to be 2% of outer dia

        self.input_cache = {'d' : d, 'D0' : D0, 'L' : L, 'Lmin' : Lmin, 
                            'Lmax' : Lmax, 'Ldelta' : Ldelta, 'h_pert' : h_pert,
                            't' : t, 'V_LRP' : V_LRP, 'H_LRP' : H_LRP, 
                            'M_LRP' : M_LRP}
        
        self.calc_cache = precalculations(self.input_cache, self.rhosteel, 
                                     self.rhowater)
        
        
    def soil_selection(self, soil_type, soil_subtype):
        #input
        #soil_type : string : sand or clay
        #soil_subtype : string : choose from the different types of soils
        self.soil_type = soil_type
        self.soil_prop = soil(soil_type, soil_subtype)
        
        
        #function to perform capacity conversions
        #output is a cache after capacity conversions. 
        self.cap_cache = cc(self.input_cache, self.calc_cache, self.soil_type, 
                       self.soil_prop, self.K)
        
     
    def checker(self, foundation_type):
        #perform installation checks
        #foundation_type     : str   : option for it to be 'anchor' or 'foundation'
        if self.soil_type.lower() == 'clay':
            self.installation_checker = installation_clay(self.soil_prop, 
                                                     self.input_cache, 
                                                     self.calc_cache, 
                                                     self.v, self.E, 
                                                     self.gamma_m, self.gamma_f)

        elif self.soil_type.lower() == 'sand':
            self.installation_checker = installation_sand(self.soil_prop, 
                                                     self.input_cache, 
                                                     self.calc_cache,
                                                     self.v, self.E, self.K, 
                                                     self.gamma_m, self.gamma_f)
        else:
            raise ValueError
         
        #perform bearing capacity checks for drained and undrained soil type    
        self.bearing_capacity_checker = bearing_capacity(foundation_type, 
                                                    self.input_cache, 
                                                    self.calc_cache, 
                                                    self.soil_prop, 
                                                    self.cap_cache, 
                                                    self.gamma_m, self.gamma_f)
        
        self.sliding_checker = sliding(self.input_cache, self.cap_cache, 
                                       self.calc_cache, self.soil_type, 
                                       self.soil_prop, self.gamma_m, 
                                       self.gamma_f)
        
# =============================================================================
#         self.uplift_checker = uplift(self.input_cache, 
#                                         self.calc_cache, 
#                                         self.soil_type,
#                                         self.soil_prop, 
#                                         self.cap_cache, self.K, 
#                                         self.gamma_m, self.gamma_f)
#                                         
# =============================================================================
                                        

        return pd.DataFrame({'L' : self.calc_cache['L'], 'h' : self.calc_cache['h'],'D' : self.calc_cache['D'], 
                'Buckling' : self.installation_checker['buckling check'],
                'Self-weight installation' : self.installation_checker['sw installation check'], 
                'Suction limit' : self.installation_checker['suction limit check'], 
                'Drained bearing capacity' : self.bearing_capacity_checker['drained bearing capacity'], 
                'Undrained bearing capacity' : self.bearing_capacity_checker['undrained bearing capacity'], 
                'Sliding' : self.sliding_checker})
    
        