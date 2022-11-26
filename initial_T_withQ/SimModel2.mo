model SimModel2 "simulation model" 
  TestModel testModel;
equation
  testModel.Tref1 = 10.0*time;
end SimModel2;
