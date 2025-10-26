import pyomo.environ as pyomo

#Part 1 = 10, Part2 = 20, Part3 = 5, Part4 = 40 
part1Width=10
part2Width=20
part3Width=5
part4Width=40

part1length=30
part2length=20
part3length=25
part4length=5

part1Cost=5
part2Cost=9
part3Cost=4
part4Cost=12

StockWidth=200
StockLength=200

# initialize the model
model = pyomo.ConcreteModel()

# define the variables
model.x1 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x2 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x3 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x4 = pyomo.Var(domain=pyomo.NonNegativeIntegers)

# define the constraints
model.c = pyomo.ConstraintList()

#Here we state the size of each piece as well as the size of the 1D stock
model.c.add((part1Width * part1length) * model.x1 + (part2Width * part2length) * model.x2 + (part3Width * part3length) * model.x3 + (part4Width * part4length) * model.x4 <= StockWidth*StockLength)

# define the objective function
obj = part1Cost * model.x1 + part2Cost * model.x2 + part3Cost * model.x3 + part4Cost * model.x4
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