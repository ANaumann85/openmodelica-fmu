# Test repository for FMU-export in open-modelica

This repository contains some test cases with simple models/equations to test the FMU export of open modelica

The test examples are:

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
