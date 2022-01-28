# Suction Caison Foundation
heavily based on OWA Suction Installed Caisson Foundations for Offshore Wind: Design Guidelines February 2019
Suction Caison foundation (SCF) module of the Selkie Project makes use of classical object oriented programing approach. Several different functions, seperately written, feed into the main class as pythonic descriptors (descriptors is an attribute of Python that can be viewed in more detail using Python's own documentation.)

Fig. 1 shows the different functions which are also the objects within the main class. The figure provides a description of the functions that make up the class. Each function within the class provides furhter description about their utility, inputs and outputs. They are also highlighted in this documentation.

Included within the documentation is a designer script which provides the user a sample script deploying the current algorithm. The user, without jumping into the code or its details, can simply alter the input parameters stated in the designer script. Care has to be taken about ensuring unit similarity, otherwise, the code will not function as desired. The default units for each input parameter is stated in the designer script and in each individual class object. Furthermore, a detailed breakdown of the inputs, outputs and their respective units, datatypes are explained in this document as well.


![](images/work_flow.pdf)
*Figure 1 shows the code architecture - the individual scripts that make up the complete algorithm, the objects that make use of these external functions and finally the class (module)*


## Version 0.00:
The designer.py sript brings together this module and functions together and provides a systematic application methodology. It provides simpler methodology for altering the input parameters and tutors in how to develop a personal script which makes use of this module.  

### Notes

The current iteration of the suction caisson makes use of hard coded soil properties. The user however, has to define the soil type and soil subtype themselves. Next revision will address this and provide more independencei in setting up proeprties. 

The module accepts a singular value of D0. Iterations over several values of D0 is achieved in the designer script - outside of this module. 
Improvements to this will be made in the next revisions

## Functions:

We will cover each function available within the SCF class, specify the inputs and outputs for them and the datatypes.


This class takes in a number of arguments. All these make it extremely important that each argument passed down is referenced with the variable definition as defined in the class.


class Foundation_Definition(): A Foundation_Definition instance is a collection of dimensions, groups, variables and attributes that together define the process to design a SCF definition.


	- def __init__(self, d, D0,  L, Lmin, Lmax, Ldelta, t, V_LRP, H_LRP, M_LRP):

This is the initialization function. To declare an instance of the class Foundation_Definition, call the class from the library foundation_characterisitcs  and pass on the directory containing the datafiles. To declare an isntance of this class, the following inputs are required:

        	- d      : float : m, water depth
        	- D0     : float : m. outer diameter
        	- D0delta: float : m, outer diameter delta
        	- L      : float : m, skirt length
        	- Lmin   : float : m, skirt length min
        	- Lmax   : float : m, skirt length max
        	- Ldelta : float : m, skirt length delta
        	- t      : float : m, wall thickness
        	- V_LRP  : float : m, vertical load reference point
        	- H_LRP  : float : m, horizontal load reference point
        	- M_LRP  : float : m, moment load reference point




	- def soil_selection(self, soil_type, soil_subtype):
	
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

		- soil_type   : string : sand or clay are acceptable options only
		- soil_subype : string : the subtypes of the two soil types



	- def checker(self, foundation_type):

Finally, the library calls the design_check function which runs 3 checks -- (1) Bearing Capacity, (2) Uplift , (3) Sliding Resistance. It however, needs no inputs. Note that this function makes use of external loads that are different from the ones calculated from slope adjustement.

	Inputs:
		- foundation_type : str : option to choose between anchor or foundation


The output of this function is a pandas dataframe with several different dimensional values. Included within the dataframe is the result of the 3 checks performed.


## Functions

This class makes use of several additional functions. Under this section, we will breakdown the objects in the class above and document the function inputs and outputs. 


	- def precalculations(input_cache, rhosteel, rhowater):
    
   		- input_cache : {} dict : dict of floats with user inputs as cache 
    		- rhosteel : float : kg/m**3, density of steel
    		- rhowater : flat : kg/m**3, water density
    
    Output
    		- cache : dict: dictionary with results of all the below calculations

