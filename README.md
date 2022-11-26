# Test repository for FMU-export in open-modelica

This repository contains some test cases with simple models/equations to test the FMU export of open modelica.

# Test models

The test models are either quadrature problems or initial value problems. The former are in folders with prefix `source`, the latter have the prefix `initial_T`. All equations are equipped with an analytical solution.

| folder | equationset | solution |
| ------ | ----------- | -------- |
| `source_withoutQ` | $\dot{T} = \lambda T_r(t)$ | $T(t) = \lambda \int_0^t T_r(\tau) d\tau$ |
|`source_withQ` | $$\dot{T} = \alpha T_r(t)$$ $$q=\alpha (T_r(t) - T)$$ | $T(t) = \lambda \int_0^t T_r(\tau) d\tau$ | 
|`initial_T_withQ` | $$\dot{T} = \alpha (T_r(t)-T)$$ $$q=-\alpha (T_r(t) - T)$$ | solution is of the form $$T(t) = T_h(t) + T_p(t)$$ with homogeneous soluton $T_h(t)$ and particular part $T_p(t)$| 

The inputs are specified in the simulation model `SimModel`:

| nr | $T_r(t)$ |
| -- | -------- |
| -  | 20t |
| 1  | 0 |
| 2  | 10t |
| 3  | 20+10t |
| 4  | 20 |

# Folder structure

Each folder contains
* a model `TestModel.mo`, which contains the basic equation
* simulation models "SimModelX.mo", where X represents the test number for the input. These simulation models are simulated with open modelica
* modelica script `buildFMU.mos`, which builds the FMUs from the `TestModel.mo`
* modelica script `simulateX.mos`, where X represents the test number for the input.
* a python module `reference.py`, which contains the reference solutions and right hand sides for each input

# Tests

Each test consists of three steps:
1. build the FMU 
2. run the simulation using omc
3. compare the modelica solution to the reference solution
4. compare the FMU solution (using fmpy) to the reference solution

All tests are run by the main workflow, where the names reflect the folder and index of the input.
