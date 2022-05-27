#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 09:36:53 2022

@author: goharshoukat
"""
import matplotlib.pyplot as plt
import pandas as pd

def plot(dimensions, soil_type):
    dimensions['installation'] = (dimensions['Suction limit'] == True) & (
        dimensions['Self-weight installation'] == True) 
    
    if soil_type == 'sand':
        dimensions['capacity'] = (dimensions['Drained bearing capacity'] == True) & (
            dimensions['Sliding'] == True
            )
    
    else:
        dimensions['capacity'] = (dimensions['Undrained bearing capacity'] == True) & (
            dimensions['Sliding'] == True
            )
        
        
        #Input
    #dimensions : pd.DataFrame : df of the relevent diensions and their
    #respective checks
    plt.figure()
    plt.scatter( dimensions['D'] , dimensions['L'],color = 'black')
    #Plot the results
    
    #insufficient capacity and uninstallable

    
    #sufficient capacitty and installable
    allTrue = dimensions[(dimensions['installation']==True) & 
                              (dimensions['capacity']==True)]
    plt.scatter(allTrue['D'], allTrue['L'], color = 'green')


    #sufficient capacity and uninstallable
    bearingTrue = dimensions[(dimensions['installation']==False) & 
                              (dimensions['capacity']==True)]
    plt.scatter(bearingTrue['D'], bearingTrue['L'], color = 'blue')
    
    
    #insufficient capacity and installable
    installTrue = dimensions[(dimensions['installation']==True) & 
                              (dimensions['capacity']==False)]
    plt.scatter(installTrue['D'],  installTrue['L'], color = 'orange')
    
    allFalse = dimensions[(dimensions['installation']==False) & 
                          (dimensions['capacity']==False)]

    plt.scatter(allFalse['D'], allFalse['L'],  color = 'red')
    

    plt.ylabel('L [m]')
    plt.xlabel(r'$D_c$ [m]')