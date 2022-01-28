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

Warning: The soil properties are hard coded. For this working version, they might not necessarily be accurate. 
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

This function performs initial calculations and dimensional adjustments from the input foundation parameters that the user adds. It takes the following as the inputs: 
    
   		- input_cache : {} dict : dict of floats with user inputs as cache 
    		- rhosteel    : float 	: kg/m**3, density of steel
    		- rhowater    : flat 	: kg/m**3, water density
    
This function outputs a dictionary of calculated dimensions from the inputs. 

    		- cache : dict: dictionary with results of all the below calculations


	- def soil(soil_type, soil_subtype):

This function is used to define the geotechnical parameters for the foundation. The geotechnical properties are hard coded and users can choose which soil type and sub type they want for the model. The inputs are:
		- soil_type  	: str : sand or clay are aceptable options only
		- soil_subtype  : str : the list of options for each soil type are shown below:

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


This function outputs a cache of soil properties: 
		- cache : {} float : dictionary of soil properties


	- def capacity_conversions(input_cache, calc_cache, soil_type, soil_prop, K):

This function provides capacity conversion calculations. It takes in the following inputs from the previous list of functions. 

    		- input_cache: {}  : dictionary of user defined inputs 
    		- soil_type  : str : string specifiying either clay or sand. 
    		- calc_cache : {}  : dictionary from the precalc function. This cache dictionary comes from the output of the functino precalculation
    		- soil_prop  : {}  : dictionary with soil properties of the sub-type. This cache dictionary comes from the output of the soil function
    		- K          : float : Constant = 0.5
 
It outputs the following:
    		
		- cache : {} float : dictionary with 3 important capacity conversion variables


	- def installation_clay(clay, input_cache, calc_cache, v, E, gamma_m, gamma_f) / def installation_sand(sand, input_cache, calc_cache, v, E, K, gamma_m, gamma_f):

These two functions are identical in their performance, however, make use of different set of equations owing to the different soil types. The function performs two step calculation: 

	Step 1: Find the setting height under self-weight of the caisson
	Step 2: Determine if the caisson with a particular height can be installed without violating the Suction Limit determined from the precalculation function. 

The inputs for both functions remains identical:

		- input_cache: dict {} : dictionary of input cache
    		- clay       : dict {} : dictionary of clay soil properties
    		- calc_cache : dict {} : dictionary of pre calculations
    		- v          : float   : pre-defined, poison ratio
    		- E          : float   : young's modulus
    		- gamma_m    : float   : ahrd coded safety factor of material
    		- gamma_f    : float   : hard coded favorable safety factor
    

This function than returns if the dimensions selected by the user will pass the installation checks and returns the results of three checks:

   		-  check      : {} boolean     : dictionary with pass/fail check for 3 installation checks. self-weight, installed height suction requirement and buckling check

	1. Installation under self-weight. 
	2. Installation using suction
	3. Buckling 


	- def bearing_capacity(foundation_type, input_cache, calc_cache, soil, cap_cache, gamma_m, gamma_f):

This function is used to determine if the dimensions specified by the user pass the bearing checks.The following are the inputs for the function:


    
		- foundation_type     : str   : option for it to be 'anchor' or 'foundation'
    		- input_cache	      : dict {} : dictionary of input cache
    		- soil       	      : dict {} : dictionary of soil properties
   		- calc_cache 	      : dict {} : dictionary of pre calculations
    		- cap_cache  	      : dict {} : dictionary of capacity cache
   		- gamma_m    	      : float   : ahrd coded safety factor of material
   		- gamma_f    	      : float   : hard coded favorable safety factor

It outputs:

		- cache  	      : {} boolean : dictionary with results of two checks: undrained bearing capacity and drained bearing capacity



	- def uplift(input_cache, calc_cache, soil_type, soil, cap_cache, K, gamma_m, gamma_f):

This functino performs checks to determine design viability from uplift forces. For each soil type, it calculates the loading and selects the minimum to compare against the threshold. The following are the comparisons it makes for each of the two soil types.

For Clay:

        1. Undrained clay
        2. Cavitation at Caisson base
        3. Cavitation under lid
        4. Friction on the sides of caisson


For Sand: 

        1. Undrained 
            a. Cavitation at footing base
            b. Cavitation below caisson lid
        2. Drained
            a. Cavitation at footing base
            b. Cavitation below caisson lid
        3. Friction on the sides of caisson


The inputs for the function are:
                
                - input_cache         : dict {} : dictionary of input cache
                - calc_cache          : dict {} : dictionary of pre calculations
                - soil_type 	      : str     : option to choose between 'clay' or 'sand'
		- soil                : dict {} : dictionary of soil properties
		- cap_cache           : dict {} : dictionary of capacity cache
                - gamma_m             : float   : ahrd coded safety factor of material
                - gamma_f             : float   : hard coded favorable safety factor


The output of this function is a vector array with booleans for the dimensions that pass or fail the threshold.


	- def sliding(input_cache, capacity_cache, calc_cache, soil_type, soil, gamma_m, gamma_f):

This function performs sliding checks for the dimensions specified. It takes the following inputs:
    
    		- input_cache: dict {} : dictionary of input cache
    		- capacity_cache : dict {} : dictionary of capacity conversion calculations
    		- clay       : dict {} : dictionary of clay soil properties
    		- calc_cache : dict {} : dictionary of pre calculations
    		- gamma_m    : float   : ahrd coded safety factor of material
    		- gamma_f    : float   : hard coded favorable safety factor


The output of this function is a vector array with booleans for the dimensions that pass or fail the threshold.



	- def plot(dimensions):

This function finally then takes the output of the dimension checks performed by the aforementioned functions/modules to present the output of the sets of dimensions that passed the checks. It has one input only:

		- dimensions : pd.DataFrame : a dataframe obtained from the output of the module foundation_characteristics which contains the L and D values and the respective results from the checks. 

It outputs a plot.         
