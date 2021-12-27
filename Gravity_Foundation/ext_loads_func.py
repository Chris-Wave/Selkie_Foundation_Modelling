#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 11:39:01 2021

@author: goharshoukat

Calculates the external loads corrected for slopes and puts them in a dictionary. 
These calculations are common for multiple classes and functions and so to avoid
repetition were seperately defined and bounded to each class individually. 

This is one of the header files for the Gravity based Foundation design for the 
Selkie Project

It is based off of Paul Bonar's adaptation of Majid Hussain's work. 



For details about the methodology, contact pbonar@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""
import math
import pandas as pd
def external_loads(slope, Mxuls, Myuls, Vuls, Huls):
    #slope : float : degrees, User defined
    #Mxuls : float : kN-m, User-defined
    #Myuls : float : kN-m, User-defined
    #Vuls  : float : kN,   User-defined
    #Huls  : float : kN,   User-defined
    #function to allocate external user defined loads to the foundation
    
    #adjust the Vuls and Huls by taking the slope effects into account
    
    #horizontal load (kN)
    Vh = Huls * math.cos(math.radians(slope)) - \
         Vuls * math.sin(math.radians(slope))
         
    #vertical load (kN)
    Vv = Huls * math.sin(math.radians(slope)) + \
         Vuls * math.cos(math.radians(slope))
    
    return {'Mxuls':Mxuls, 'Myuls':Myuls, 'Vv':Vv, 'Vh':Vh}