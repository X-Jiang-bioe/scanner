# doe_tool

Small lightweight package to simplify Design Of Expermient(DOE) simulations, i.e.
parameter scanning for a given model

## Usage instructions

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

        outputs of the example function
        ```
        ex_scan.get_outputs()
        ```
        parameter values used (id of iterables correlate)
        ```
        ex_scan.get_simspecs()
        ```




