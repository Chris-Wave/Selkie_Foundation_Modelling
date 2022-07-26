#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 15:50:02 2021

@author: goharshoukat


Soil properties are predefined in this script. This feeds into the foundation_
characteristics class.  

This is the main library description for the suction caisson Foundation design for the 
Selkie Project

This code is based off of Christopher Wright's work on suction caisson 



For details about the methodology, contact cwrigth@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 
"""

import math

def soil(soil_type, soil_subtype):
    #input
    #soil_type  : string : sand or clay are acceptable options only
    #soil_subype : string : 
    """
    For the soil type of clay, the following subtypes are possible:
        1. very soft
        2. soft
        3. firm
        4. stiff
        5. very stiff
        6. hard
    
    For the soil type of sand, the follwing subtypes are possible:
        1. very loose
        2. loose
        3. medium dense
        4. dense
        5. very dense
        
    """
    
    #output
    #soil_parameters : dictionary : dictionary of soil parameters. the cache
    #is different for the two types included in this script
    
    Nc  =  math.pi + 2      #bearing capacity factor cohesion


    if soil_type.lower() == 'clay':
        phi = 0
        if soil_subtype.lower() == 'extremely low strength':
            s_u = 1E4               #Undrained strength
            s_t = 2                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 7.0362E3             #effective unit weight of soil N/m3
            #Nq = 10.6
            
        
        if soil_subtype.lower() == 'very low strength':
            s_u = 1.5E4               #Undrained strength
            s_t = 2                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 7.0362E3             #effective unit weight of soil N/m3
            #Nq = 10.6
        
       
        if soil_subtype.lower() == 'low strength':
            s_u = 3E4               #Undrained strength
            s_t = 1.5                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 7.0362E3             #effective unit weight of soil N/m3
            #Nq = 10.6
        
        if soil_subtype.lower() == 'medium strength':
            s_u = 5.0E4               #Undrained strength
            s_t = 1.5               #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 9.6138E3             #effective unit weight of soil N/m3
            #Nq = 10.6
        
        if soil_subtype.lower() == 'high strength':
            s_u = 10E4               #Undrained strength
            s_t = 1.2                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 9.6138E3             #effective unit weight of soil N/m3
            #Nq = 10.6
        
        if soil_subtype.lower() == 'very high strength':
            s_u = 20E4               #Undrained strength
            s_t = 1.2                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 9.6138E3             #effective unit weight of soil N/m3
            #Nq = 10.6
        
        return {'s_u':s_u, 's_t' : s_t,'alpha' : alpha,
                'gamma' : gamma,'Nc' : Nc, 'phi' : phi}
             
    
    
    
    
    
    
    
    else: #sand
        if soil_subtype.lower() == 'very loose':
            gamma = 8.5347E3                                 #Effective unit weight of soil
            phi = math.radians(25)                      #angle of friction
            rel_density_index = 0.1                     #relative density index
            delta = math.radians(math.degrees(phi) - 5) #interface friction angle
                                       #bearing capacity factor (overburden)
            
            
            #missing properties copied from clay above 
            #these properties are missing from the table and prevent
            #algorithm execution
            
            s_u = 2E4
            
        elif soil_subtype.lower() == 'loose':
            gamma = 8.5347E3                                 #Effective unit weight of soil
            phi = math.radians(30)                      #angle of friction
            rel_density_index = 0.25                    #relative density index
            delta = math.radians(math.degrees(phi) - 5) #interface friction angle
                                       #bearing capacity factor (overburden)
            
            #missing properties copied from clay above 
            #these properties are missing from the table and prevent
            #algorithm execution
            
            s_u = 3E4
            
            
        
        
        
        elif soil_subtype.lower() == 'medium dense':
            gamma = 8.5347E3                                 #Effective unit weight of soil
            phi = math.radians(32)                      #angle of friction
            rel_density_index = 0.45                    #relative density index
            delta = math.radians(math.degrees(phi) - 5) #interface friction angle
           
            
            #missing properties copied from clay above 
            #these properties are missing from the table and prevent
            #algorithm execution
            
            s_u = 4E4
            
            
   
            
        elif soil_subtype.lower() == 'dense':
            gamma = 10.3986E3                                 #Effective unit weight of soil
            phi = math.radians(35)                      #angle of friction
            rel_density_index = 0.75                    #relative density index
            delta = math.radians(math.degrees(phi) - 5) #interface friction angle
           
            #missing properties copied from clay above 
            #these properties are missing from the table and prevent
            #algorithm execution
            
            s_u = 5E4
            
            
        else:
            gamma = 10.3986E3                                 #Effective unit weight of soil
            phi = math.radians(38)                      #angle of friction
            rel_density_index = 0.85                    #relative density index
            delta = math.radians(math.degrees(phi) - 5) #interface friction angle
            
            
            #missing properties copied from clay above 
            #these properties are missing from the table and prevent
            #algorithm execution
            
            s_u = 6E4
            
            
            
        return {'gamma':gamma, 'phi':phi, 'rel_density_index':rel_density_index,
                'delta':delta, 
                 'Nc' : Nc, 's_u' : s_u}
