#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 16:32:11 2021

@author: goharshoukat

function untested, unintegrated. 
"""
import  math
import numpy as np
def bearing_capacity(ty, condition, M_LRP, L, cache, capacity_cache, clay_prop,
                     sand_prop, gamma_m, gamma_f):
    #Input
    #ty     : str   : option for it to be 'anchor' or 'foundation'
    #condition : str : option to chose between drained or undrained
    #M_LRP  : float : m, moment load reference points
    #cache  : dict {} : dictionary of pre calculations
    #L      : float   : m, skirt length
    #clay_prop : dict : cache with clay proeprties
    #sand_prop : dict : cache with sand proeprties
    #gamma_m : float : safety factor of materia 
    #gamma_f : float : favorouble safety factor load
    
    
    if ty.lower() == 'anchor' or M_LRP == 0:
        Aeff = math.pi * cache['D']**2 / 4
        Beff = cache['D']
        Leff = Beff
        
    elif ty.lower() == 'foundation' or M_LRP > 0:
        e = capacity_cache['Mbase'] / capacity_cache['Vbase']
        Aeff = 2*(cache['D']/4 * math.acos(2 * e / cache['D']) - e * 
                  math.sqrt(cache['D']**2 / 4 - e**2))
        Be = cache['D'] - 2*e
        Le = math.sqrt(cache['D']**2 - (cache['D'] - Be)**2)
        Leff = math.sqrt(Aeff * Le / Be)
        Beff = math.sqrt(Aeff * Be/Le)
    
    else:
        raise ValueError
        
        
        
    h = np.linspace(int(cache['h']), int(cache['h'] + 50), int((cache['h']+50)))   
    if condition.lower() == 'undrained':
        Nc = 2 + math.pi
        ica = 0.5 - 0.5 * math.sqrt(1 - capacity_cache['Hbase']/(
            Aeff * clay_prop['s_u']))
        sca = 0.2 * ( 1 -2 * ica) * Beff/Leff
        dca = 0.3 * np.arctan(h/Beff)
        Vbase_R = Aeff * (clay_prop['Nc'] * clay_prop['s_u']*(1 + sca + dca - 
                                    ica) + sand_prop['gamma'] * h)
        
        
        
        
        