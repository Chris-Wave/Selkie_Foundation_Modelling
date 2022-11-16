#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 16:12:26 2022

@author: goharshoukat


This script will sequentially perform several checks on different locations
of the caisson to determine if the design passes checks

Feeds into the Foundation_characteristic

This script is used to calculte the eccentricity checks
"""
import numpy as np
import math
import logging
def eccentricity(input_cache, calc_cache, cap_cache, mooring_cache):
    #Inputs
    #input_cache : {}  : dictioinary with input cache    
    #calc_cache  : {}  : dictionary with precalculations
    #cap_cache  : {}  : dictionary with capacity conversions
    #mooring_cache : {} : inputs from mooring calcculations
    
    #output
    #returns an outpyt vector of boolean. True if condition is satisfied. 
    
    #checks are only performed if solution for Ta converges in precalcs, otherwise
    #the check passes as Hd and Vd would be zero and less than 1
    
    #Angle theta_a must be less than 90 degrees.
    if calc_cache['Ta'] != 0 and calc_cache['theta_a']< math.pi/2:
        Hd = calc_cache['Ta'] * np.cos(calc_cache['theta_a'])
        Vd = calc_cache['Ta'] * np.sin(calc_cache['theta_a'])
        
        a = calc_cache['h'] / calc_cache['D'] + 0.5#a = input_cache['L'] / calc_cache['D'] + 0.5
        b = calc_cache['h'] / (3 * calc_cache['D']) + 4.5#b = input_cache['L'] / (3 * calc_cache['D']) + 4.5
        
        logging.info('**** \nEccentricity Checks ****')
        logging.info('\nHd = {}\nVd = {}\na = {}\nb = {}'.format(Hd, Vd, a, b))
        logging.info('\nEccentricity check = {}'.format(((Hd/cap_cache['Hu_dto'])**a + (Vd / cap_cache['Vu_dto'])**b ) < 1))
       # print('left-side = {}'.format(Hd/mooring_cache['Huls'])**a + (Vd / mooring_cache['Vuls'])**b)
        return ((Hd/cap_cache['Hu_dto'])**a + (Vd / cap_cache['Vu_dto'])**b ) < 1
    else:
        logging.info('\nEccentricity check = True')
        return True