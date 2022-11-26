model TestModel "test model"

  Real T;
  input Real Tref1 "reference Temperature";
  parameter Real alpha1 = 10;
  parameter Real T0 = 0 "start value for T";
initial equation
  T = T0;
equation
   der(T) = alpha1*Tref1; 
end TestModel;
