#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 09:36:53 2022

@author: goharshoukat
"""
import matplotlib.pyplot as plt
import pandas as pd

def plot(dimensions):
    #Input
    #dimensions : pd.DataFrame : df of the relevent diensions and their
    #respective checks
    plt.scatter(dimensions['D'], dimensions['L'], color = 'black')
    #Plot the results
    allFalse = dimensions[(dimensions['Buckling']==False) & 
                    
                     (dimensions['Sliding']==False) &
                     (dimensions['Drained bearing capacity']==False) &
                     (dimensions['Undrained bearing capacity']==False) &
                     (dimensions['Self-weight installation']==False) &
                     (dimensions['Suction limit']==False)]

    plt.scatter(allFalse['D'], allFalse['L'], color = 'red')
    
    
    allTrue = dimensions[(dimensions['Buckling']==True) & 
                     
                     (dimensions['Sliding']==True) &
                     (dimensions['Drained bearing capacity']==True) &
                     (dimensions['Undrained bearing capacity']==True) &
                     (dimensions['Self-weight installation']==True) &
                     (dimensions['Suction limit']==True)]
    plt.scatter(allTrue['D'], allTrue['L'], color = 'green')

    bearingTrue = dimensions[(dimensions['Drained bearing capacity']==True) & 
                             (dimensions['Undrained bearing capacity']==True) & 
                             (dimensions['Self-weight installation']==False) &
                             (dimensions['Buckling']==False) & 
                             (dimensions['Suction limit']==False)]
    plt.scatter(bearingTrue['D'], bearingTrue['L'], color = 'orange')
    
    installTrue = dimensions[(dimensions['Drained bearing capacity']==False) & 
                             (dimensions['Undrained bearing capacity']==False) & 
                             (dimensions['Self-weight installation']==True) &
                             (dimensions['Buckling']==True) & 
                             (dimensions['Suction limit']==True)]
    plt.scatter(installTrue['D'], installTrue['L'], color = 'yellow')
    
    

    plt.xlabel('L [m]')
    plt.ylabel('D [m]')