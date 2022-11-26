model SimModel "simulation model" 
  TestModel testModel;
equation
  testModel.Tref1 = 20.0*time;
end SimModel;
