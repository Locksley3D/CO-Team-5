import pyomo.environ as pyomo

# initialize the model
model = pyomo.ConcreteModel()

# define the variables
model.x1 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x2 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x3 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x4 = pyomo.Var(domain=pyomo.NonNegativeIntegers)

# define the constraints
model.c = pyomo.ConstraintList()
model.c.add(13 * model.x1 + 21 * model.x2 + 17 * model.x3 + 100 * model.x4 <= 10000)
model.c.add(model.x1 <= 1000)
model.c.add(model.x2 <= 400)
model.c.add(model.x3 <= 500)
model.c.add(model.x4 <= 150)

# define the objective function
obj = 6 * model.x1 + 10 * model.x2 + 8 * model.x3 + 40 * model.x4
model.objective = pyomo.Objective(sense = pyomo.maximize, expr = obj)

# select a solver
solver = pyomo.SolverFactory('gurobi')

# solve the problem
result = solver.solve(model, tee=True)

print("-----Printing the model-----")
model.pprint()
print("-----Printing the results-----")
print(result)
print("-----Printing the values of the optimal solution-----")
print("x1 = ", model.x1(), " - x2 = ", model.x2(), " - x3 = ", model.x3(), " - x4 = ", model.x4(), " - z = ", model.objective())