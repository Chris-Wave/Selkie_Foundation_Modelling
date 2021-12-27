#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 11:43:20 2021

@author: goharshoukat

This is the Gravity based foundation designer script

It makes use of the foundation_characterisitcs class

It defines the soil properties and foundation dimensions

The backend performs the necessary calculations to see if this design
will pass the necessary checks

It will then return an array with different diimensions which pass each of the
three tests. Further array manipulation will is then handled here which will then
provide the smallest dimensions which pass all three tests
"""

import numpy as np
import math
import pandas as pd
from foundation_characteristics import Foundation_Definition

"""
The following properties must be defined in order to get the calculations going

1. Weight of Concrete [kN/m**3]
2. Weight of slag [kN/m**3]
3. Slope [degrees]
4. Device Geometry [m]
5. Safety Factor for bearing capacity


The next set of inputs required will be stated when the specific portion of the
code is reached 
"""

#Values here are only assumed and might not present any realistic picture
weight_concrete = 
weight_slag
slope = 
device_geometry
SF
#declare FoundationA to be an instance of the class
Foundation_A = Foundation_Definition()

