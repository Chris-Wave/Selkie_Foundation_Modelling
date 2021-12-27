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
    
    if soil_type.lower() == 'clay':
        if soil_subtype.lower() == 'very soft':
            s_u = 1E4               #Undrained strength
            s_t = 12                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 720             #effective unit weight of soil
            Nc  =  5.141592654      #bearing capacity factor cohesion
            
        elif soil_subtype.lower() == 'soft':
            s_u = 2E4               #Undrained strength
            s_t = 12                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 720             #effective unit weight of soil
            Nc  =  5.141592654      #bearing capacity factor cohesion
            
        elif soil_subtype.lower() == 'firm':
            s_u = 3.3E4               #Undrained strength
            s_t = 12                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 720             #effective unit weight of soil
            Nc  =  5.141592654      #bearing capacity factor cohesion
        
        
        elif soil_subtype.lower() == 'stiff':
            s_u = 7.5E4               #Undrained strength
            s_t = 12                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 980             #effective unit weight of soil
            Nc  =  5.141592654      #bearing capacity factor cohesion
            
            
        elif soil_subtype.lower() == 'very stiff':
            s_u = 1.5E5               #Undrained strength
            s_t = 12                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 980             #effective unit weight of soil
            Nc  =  5.141592654      #bearing capacity factor cohesion
            
        else:
            s_u = 2E5               #Undrained strength
            s_t = 12                #soil sensitivity
            alpha = 1/s_t           #adhesion factor
            gamma = 980             #effective unit weight of soil
            Nc  =  5.141592654      #bearing capacity factor cohesion
        
        return {'s_u':s_u, 's_t' : s_t,'alpha' : alpha,'gamma' : gamma,'Nc' : Nc}
    
    
    
    
    
    
    
    else: #sand
        if soil_subtype.lower() == 'very loose':
            gamma = 870             #Effective unit weight of soil
            phi = 25                  #angle of friction
            rel_density_index = 0.1    #relative density index
            delta = phi - 5         #
            Nq = 10.66214239           #bearing capacity factor (overburden)
            
            
        elif soil_subtype.lower() == 'loose':
            gamma = 870             #Effective unit weight of soil
            phi = 30                  #angle of friction
            rel_density_index = 0.25     #relative density index
            delta = phi - 5         #
            Nq = 18.40112222           #bearing capacity factor (overburden)
            
        elif soil_subtype.lower() == 'medium dense':
            gamma = 870             #Effective unit weight of soil
            phi = 32                   #angle of friction
            rel_density_index = 0.45     #relative density index
            delta = phi - 5         #
            Nq = 23.17677621           #bearing capacity factor (overburden)
            
   
            
        elif soil_subtype.lower() == 'dense':
            gamma = 870             #Effective unit weight of soil
            phi = 35                  #angle of friction
            rel_density_index = 0.75     #relative density index
            delta = phi - 5         #
            Nq = 33.29609149           #bearing capacity factor (overburden)
            
            
        else:
            gamma = 870             #Effective unit weight of soil
            phi = 38                   #angle of friction
            rel_density_index = 0.85    #relative density index
            delta = phi - 5         #
            Nq = 48.9332527           #bearing capacity factor (overburden)
            
        return {'gamma':gamma, 'phi':phi, 'rel_density_index':rel_density_index,
                'delta':delta, 'Nq':Nq}