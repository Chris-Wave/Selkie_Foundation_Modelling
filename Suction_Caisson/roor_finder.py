#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:58:54 2022

@author: goharshoukat
"""

import math
import matplotlib.pyplot as plt
import numpy as np
# =============================================================================
# a = [0.13]
s = np.arange(-2.5E7, 6e5, 10000)
# i = 0
# Z0 = 2.16
# Zi = 1.71
# Nq = 33.2
# K = 0.5
# Ngamma = 33.9
# =============================================================================

#solving for suction
Routside = (sand['gamma'] + (a[i] * s / calc_cache['h'][i])) * Z0**2 * (
    np.exp(calc_cache['h'][i] / Z0) - 1 - calc_cache['h'][i] / Z0)\
    * (K * math.tan(sand['delta'])) * math.pi * input_cache['D0']

Rinside = (sand['gamma'] - (((1 - a[i]) * s) / calc_cache['h'][i])) * \
    Zi**2 * (np.exp(calc_cache['h'][i] / Zi) - 1 - 
             (calc_cache['h'][i] / Zi))\
    * (K * math.tan(sand['delta'])) * math.pi * calc_cache['Di']

Rtip = ((sand['gamma'] - (((1 - a[i]) * s) / calc_cache['h'][i])) * Zi * (
    np.exp(calc_cache['h'][i] / Zi) - 1) * Nq + sand['gamma'] * 
    input_cache['t'] * Ngamma) * math.pi * input_cache['t'] * calc_cache['D']

RTotal = (Routside + Rinside + Rtip - calc_cache['V_comma']) / calc_cache['Ac']


plt.plot(s, RTotal)
plt.plot(s, np.zeros(len(s)))
plt.xlabel('suction')
plt.ylabel('Resistance')


#solve for self-weight, h
h = np.arange(0,10 , 1)
Routside =  sand['gamma'] * Z0**2 * (np.exp(h / Z0) - 1 - (h / Z0)) * (
    K * math.tan(sand['delta'])) * (math.pi * input_cache['D0'])

Rinside = sand['gamma'] * Zi**2 * (np.exp(h / Zi) - 1 - h / Zi) * (
    K * math.tan(sand['delta'])) * math.pi * calc_cache['Di']

Rtip =  (sand['gamma'] * Zi * (np.exp(h / Zi) - 1) * Nq +
         sand['gamma'] * input_cache['t'] * Ngamma) *  math.pi * \
            calc_cache['D'] * input_cache['t']
RTotal = (Routside + Rinside + Rtip) - calc_cache['V_comma']


plt.plot(h, RTotal, alpha=0.5)
plt.plot(h, np.zeros(len(h)), alpha = 0.5)
plt.xlabel('height')
plt.ylabel('Resistance')
plt.show()
