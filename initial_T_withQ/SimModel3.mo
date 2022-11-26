model SimModel3 "simulation model" 
  TestModel testModel;
equation
  testModel.Tref1 = 20.0 + 10*time;
end SimModel3;
