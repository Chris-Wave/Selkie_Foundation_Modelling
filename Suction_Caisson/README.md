# Suction Caison Foundation
Suction Caison foundation (SCF) module of the Selkie Project makes use of classical object oriented programing approach. Several different functions, seperately written, feed into the main class as pythonic descriptors (descriptors is an attribute of Python that can be viewed in more detail using Python's own documentation.)

Fig. 1 shows the different functions which are also the objects within the main class. The figure provides a description of the functions that make up the class. Each function within the class provides furhter description about their utility, inputs and outputs. They are also highlighted in this documentation.

Included within the documentation is a designer script which provides the user a sample script deploying the current algorithm. The user, without jumping into the code or its details, can simply alter the input parameters stated in the designer script. Care has to be taken about ensuring unit similarity, otherwise, the code will not function as desired. The default units for each input parameter is stated in the designer script and in each individual class object. Furthermore, a detailed breakdown of the inputs, outputs and their respective units, datatypes are explained in this document as well.


![](images/work_flow.pdf)
*Figure 1 shows the code architecture - the individual scripts that make up the complete algorithm, the objects that make use of these external functions and finally the class (module)*


## Version 0.00:
Warning: This version is not a stable released version. It is work in progress.

The current iteration of the suction caisson makes use of hard coded soil properties. The user however, has to define the soil type and soil subtype themselves. Next revision will address this and provide more independencei in setting up proeprties. 

The module accepts a singular value of D0. Iterations over several 
values of D0 is achieved in the designer script - outside of this module. 
Improvements to this will be made in the next revisions

## Functions:

We will cover each function available within the SCF class, specify the inputs and outputs for them and the datatypes.


This class takes in a number of arguments. All these make it extremely important that each argument passed down is referenced with the variable definition as defined in the class.


class Foundation_Definition(): A Foundation_Definition instance is a collection of dimensions, groups, variables and attributes that together define the process to design a SCF definition.


	- def __init__(self, d, D0, D0min, D0max, D0delta, L, Lmin, Lmax, Ldelta, t, V_LRP, H_LRP, M_LRP):

This is the initialization function. To declare an instance of the class Foundation_Definition, call the class from the library foundation_characterisitcs  and pass on the directory containing the datafiles. To declare an isntance of this class, the following inputs are required:

        	- d      : float : m, water depth
        	- D0     : float : m. outer diameter
        	- D0min  : float : m, outer diameter min
        	- D0max  : float : m, outer diameter max
        	- D0min  : float : m, outer diameter min
        	- D0delta: float : m, outer diameter delta
        	- L      : float : m, skirt length
        	- Lmin   : float : m, skirt length min
        	- Lmax   : float : m, skirt length max
        	- Ldelta : float : m, skirt length delta
        	- t      : float : m, wall thickness
        	- V_LRP  : float : m, vertical load reference point
        	- H_LRP  : float : m, horizontal load reference point
        	- M_LRP  : float : m, moment load reference point



	- def precalculations(d, D0, L, t, rhosteel, rhowater, V_LRP):
    #input
    - d    : float : m, depth
    - D0   : float : m, outer diameter
    - L    : float : m, skirt length
    - t    : float : m, wall thickness 
    - rhosteel : float : kg/m**3, density of steel
    - rhowater : flat : kg/m**3, water density
    - V_LRP  : float : m, vertical load reference point
    
    #output
    #cache : dict: dictionary with results of all the below calculations




	- def sliding(capacity_cache, cache, soil_type, sand_prop, clay_prop, gamma_m, H_LRP):

This function is used to check for the sliding resistance of the foundation design. It takes the following inputs:
     
    		- soil_type : str : string specifiying either clay or sand
    		- cache     : {}  : dictionary from the precalc function
    		- soil_prop: {}  : dictionary with soil properties of the sub-type 
    		- clay_prop : dict : cache with clay proeprties
    		- sand_prop : dict : cache with sand proeprties
    		- gamma_m   : float : material safety factor
    		- H_LRP  : float : m, horizontal load reference point


	- def soil(soil_type, soil_subtype):

The algorithm provides option to choose between sand and clay. Further subtypes of each of the two soil classifications is provided. For the clay type soil, the following can be selected:
the following subtypes are possible:
        1. very soft
        2. soft
        3. firm
        4. stiff
        5. very stiff
        6. hard

For the sand type, the following subtypes are possible:
        1. very loose
        2. loose
        3. medium dense
        4. dense
        5. very dense

The function takes in two arguments:

		- soil_type  : string : sand or clay are acceptable options only
		- soil_subype : string : 


def uplift(soil_type, analysis_type, capacity_cache, cache , sand_prop, 
           clay_prop, K):
    #Input
    #soil_type : str : string specifiying either clay or sand-drained, sand-undrained
    #cache     : {}  : dictionary from the precalc function
    ##soil_prop: {}  : dictionary with soil properties of the sub-type 
    #clay_prop : dict : cache with clay proeprties
    #sand_prop : dict : cache with sand proeprties
    #analysis_type : str : option to chose between undrained, cavitation-lid and
    #                                                           cavitation-base
    #K         : float : constant user specified
