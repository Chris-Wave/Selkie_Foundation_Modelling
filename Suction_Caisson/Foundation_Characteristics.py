#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:08:33 2021

@author: goharshoukat

Foundation properties and material characteristics are defined in this class. 

This is the main library description for the suction caisson Foundation design for the 
Selkie Project

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""
import math
from precalculation import precalculations
    
    
class Foundation_Definition:
    
    gravity     = 9.81
    K           = 0.5
    v           = 0.3 #poisson ratio
    rhosteel    = 8050 
    E           = 210E6    #young's modulus
    rhowater    = 1025 #density of water
    
    def __init__(self, d, D0, D0min, D0max, D0delta, L, Lmin, Lmax, Ldelta, t, 
                 V_LRP):
        #inputs
        #d      : float : m, water depth
        #D0     : float : m. outer diameter
        #D0min  : float : m, outer diameter min
        #D0max  : float : m, outer diameter max
        #D0min  : float : m, outer diameter min
        #D0delta: float : m, outer diameter delta
        #L      : float : m, skirt length
        #Lmin   : float : m, skirt length min
        #Lmax   : float : m, skirt length max
        #Ldelta : float : m, skirt length delta
        #t      : float : m, wall thickness
        #V_LRP  : float : m, vertical load reference point
        
        self.d = d
        self.D0 = D0
        self.D0min = D0min
        self.D0max = D0max
        self.D0delta = D0delta
        self.L = L
        self.Lmin = Lmin 
        self.Lmax = Lmax
        self.Ldelta = Ldelta
        self.t = t
        self.V_LRP = V_LRP
        self.cache = precalculations(d, D0, L, t, self.rhosteel, self.rhowater,
                                     V_LRP)
        
        
        
        
        
        #
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        ##
        #
        #
        #
A = Foundation_Definition(10, 12, 13, 10, 1 , 2, 3, 3, 3, 4,2)        
x = A.cache
