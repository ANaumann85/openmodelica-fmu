# Test repository for FMU-export in open-modelica

This repository contains some test cases with simple models/equations to test the FMU export of open modelica

The test examples are:

| folder | equationset | solution |
| ------ | ----------- | -------- |
| `source_withQ` | $\dot{T} = \lambda T_r(t)$ | $T(t) = \lambda \int_0^t T_r(\tau) d\tau$ |
|`source_withQ` | $$\dot{T} = \alpha T_r(t)$$ $$q=\alpha (T_r(t) - T)$$ | | $T(t) = \lambda \int_0^t T_r(\tau) d\tau$ | 

The inputs are specified in the simulation model `SimModel`:

| nr | $T_r(t)$ |
| -- | -------- |
| -  | $T_r(t) = 20 t$ |
