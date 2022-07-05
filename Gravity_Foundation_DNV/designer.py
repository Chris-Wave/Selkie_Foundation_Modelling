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
weight_concrete     = 0 
weight_slag         = 0
slope               = 0
device_geometry     = 3
SF                  = 1
#declare FoundationA to be an instance of the class
Foundation_A = Foundation_Definition(weight_concrete, weight_slag, slope, 
                                     device_geometry, SF)

"""
After class decleration, select soil properties. For undrained soil, the 
following parameters need to be declared. 
1. friction angle [degrees]
2. cohesion [kPa]
3. factor of safety for soil parameters
4. relative_density [%]
5. weight [kN/m**3]
6. sensitivity

Decleration of soil functtion does not return any value, however, it enables
the next set of functions to perform their calculations and produce a cache
of results
"""
#define the soil parameters
friction_angle      = 35 
cohesion            = 50
fos                 = 1
relative_density    = 65
weight              = 19
sensitivity         = 5

#For undrained, use the following: 
#Foundation_A.undrained_soil(friction_angle, cohesion, fos, relative_density, 
#                            weight, sensitivity)

#For drained, use the following: (commented out)
    
Foundation_A.drained_soil(friction_angle, cohesion, fos,
                          weight, sensitivity)

"""
External loading needs to be defined in the next function call
The variables required are:
1. Mxuls [kN-m]
2. Myuls [kN-m]
3. Vuls [kN]
4. Huls [kN-m]
"""
Mxuls               = 1000
Myuls               = 0
Vuls                = 1000
Huls                = 1000
Foundation_A.external_loads(Mxuls, Myuls, Vuls, Huls)


"""
After the load definition, eccentricity calculations need to be performed
Eccentricity calculations will take all class objects to complete calculations.
The function needs to be called however. 

Following the eccentricity calculation, presence of key needs to
be defined. this function takes a string - yes or no. 

Simultaenously, it is important to define if embedment is present. The function
takes in a string, y or n. 
"""
Foundation_A.eccentricity()
Foundation_A.key_calc('n')
Foundation_A.embedment('n')

"""
Finally, the smallest dimension that clears all checks are identified. 
If in an nth iteration, no dimension which passes all three checks is obtained,
nth + 1 iteration is performed. 

The designe_check method is called and it returns the dimensions with their 
checks. 
"""
dimensions = Foundation_A.design_check()
