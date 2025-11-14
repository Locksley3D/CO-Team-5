import pyomo.environ as pyomo
import csv


#Part 1 = 10, Part2 = 20, Part3 = 5, Part4 = 40 

part1length=30
part2length=20
part3length=25
part4length=50

part1Gain=5
part2Gain=9
part3Gain=4
part4Gain=12

part1DemandLower = 5 
part2DemandLower = 7
part3DemandLower = 20
part4DemandLower = 16

part1DemandUpper = 6 
part2DemandUpper = 8
part3DemandUpper = 22
part4DemandUpper = 18

StockLength = 200 # 9 stocks
StockCost =  50

# initialize the model
model = pyomo.ConcreteModel()

# define the variables
model.x1 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x2 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x3 = pyomo.Var(domain=pyomo.NonNegativeIntegers)
model.x4 = pyomo.Var(domain=pyomo.NonNegativeIntegers)

model.z1 = pyomo.Var(domain=pyomo.Binary)
model.z2 = pyomo.Var(domain=pyomo.Binary)
model.z3 = pyomo.Var(domain=pyomo.Binary)
model.z4 = pyomo.Var(domain=pyomo.Binary)
model.z5 = pyomo.Var(domain=pyomo.Binary)
model.z6 = pyomo.Var(domain=pyomo.Binary)
model.z7 = pyomo.Var(domain=pyomo.Binary)
model.z8 = pyomo.Var(domain=pyomo.Binary)
model.z9 = pyomo.Var(domain=pyomo.Binary)


# define the constraints
model.c = pyomo.ConstraintList()

#Here we state the size of each piece as well as the size of the 1D stock
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z1)
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z2)
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z3)
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z4)
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z5)
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z6)
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z7)
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z8)
model.c.add(part1length * model.x1 + part2length * model.x2 + part3length * model.x3 + part4length * model.x4 <= StockLength * model.z9)

model.c.add(model.x1 >= part1DemandLower)
model.c.add(model.x1 <= part1DemandUpper)
model.c.add(model.x2 >= part2DemandLower)
model.c.add(model.x2 <= part2DemandUpper)
model.c.add(model.x3 >= part3DemandLower)
model.c.add(model.x3 <= part3DemandUpper)
model.c.add(model.x4 >= part4DemandLower)
model.c.add(model.x4 <= part4DemandUpper)

# define the objective function
obj = part1Gain * model.x1 + part2Gain * model.x2 + part3Gain * model.x3 + part4Gain * model.x4 - StockCost * model.z1 - StockCost * model.z2 - StockCost * model.z3 - StockCost * model.z4 - StockCost * model.z5 - StockCost * model.z6 - StockCost * model.z7 - StockCost * model.z8 - StockCost * model.z9
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
