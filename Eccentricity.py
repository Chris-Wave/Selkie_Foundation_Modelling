#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 15:17:04 2021

@author: goharshoukat

This function calculates the eccentricity and will be utilised using descriptors

This function feeds into the class foundation characteristics

THis script is part of the Selkie Project

It is based off of Paul Bonar's adaptation of Majid Hussain's work. 

For details about the methodology, contact pbonar@gdgeo.com
For questions regarding the code, please contact gshoukat@gdgeo.com 

"""

import math
import numpy as np

def eccent(ex, ey, Ix_min, Iy_min):
    
    