# doe_tool

Small lightweight package to simplify Design Of Expermient(DOE) simulations, i.e.
parameter scanning for a given model. Supports SBML and antimony models as is.


## Usage instructions
0. ### For the SBML/Antomony and more details, see the demo.ipynb

1. ### Function requirements:

    For the tool to work correctly, one needs to setup the function that accepts simulation specifications of the following form:
    ```
    simspecs = {'name_of_parameter' : parameter_value}
    ```
    A simple example that raises x to the y-th power:
    ```
    def examplefun(simspecs):
        return simspecs['x'] ** simspecs['y']
    ```
2. ### Setup:

    Following the simple example above:

    ```
    parameter_names = ('x', 'y')
    initial_values = (1, 1)
    ex_scan = doe_tool(examplefun, parameter_names, initial_values)
    ```

3. ### Usage:

    * to run a scan:
        ```
        scan_parameters = (('x', (1,2,3)),
                            'y', (4,5,6)))
        ex_scan.scan(scan_paramneters)
        ```
    * extracting information:

        To get the information from scan
        ```
        specs, sims, results = ex_scan.get_scan()
        ```
        specs are the parameter calues used in a given run
        sims are the simulations
        results are outputs from a post processor(if one was created)
        




