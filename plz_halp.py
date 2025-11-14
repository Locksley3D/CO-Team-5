import pyomo.environ as pyomo

# ----------------------
# Data
# ----------------------
part_lengths = [30, 20, 25, 50]       # Length of each part
part_gains = [5, 9, 4, 12]            # Profit of each part
demand_lower = [5, 7, 20, 16]         # Minimum demand
demand_upper = [6, 8, 22, 18]         # Maximum demand

StockLength = 200
StockCost = 50
num_stocks = 9
num_parts = len(part_lengths)

# ----------------------
# Initialize model
# ----------------------
model = pyomo.ConcreteModel()

# Sets
model.parts = pyomo.RangeSet(0, num_parts-1)
model.stocks = pyomo.RangeSet(0, num_stocks-1)

# Variables
# x[i,j] = number of parts i in stock j
model.x = pyomo.Var(model.parts, model.stocks, domain=pyomo.NonNegativeIntegers)

# z[j] = whether stock j is used
model.z = pyomo.Var(model.stocks, domain=pyomo.Binary)

# ----------------------
# Constraints
# ----------------------

# 1. Stock capacity constraints
def stock_capacity_rule(model, j):
    return sum(part_lengths[i] * model.x[i,j] for i in model.parts) <= StockLength * model.z[j]
model.stock_capacity = pyomo.Constraint(model.stocks, rule=stock_capacity_rule)

# 2. Demand lower bounds
def demand_lower_rule(model, i):
    return sum(model.x[i,j] for j in model.stocks) >= demand_lower[i]
model.demand_lower = pyomo.Constraint(model.parts, rule=demand_lower_rule)

# 3. Demand upper bounds
def demand_upper_rule(model, i):
    return sum(model.x[i,j] for j in model.stocks) <= demand_upper[i]
model.demand_upper = pyomo.Constraint(model.parts, rule=demand_upper_rule)

# ----------------------
# Objective function
# ----------------------
model.profit = pyomo.Objective(
    expr=sum(part_gains[i] * model.x[i,j] for i in model.parts for j in model.stocks)
         - sum(StockCost * model.z[j] for j in model.stocks),
    sense=pyomo.maximize
)

# ----------------------
# Solve the model
# ----------------------
solver = pyomo.SolverFactory('gurobi')
result = solver.solve(model, tee=True)

# ----------------------
# Display results
# ----------------------
print("\n----- Optimal Total Parts -----")
for i in model.parts:
    total_i = sum(model.x[i,j]() for j in model.stocks)
    print(f"Part {i+1}: {total_i}")

print("\n----- Stocks Used and Parts in Each Stock -----")
for j in model.stocks:
    if model.z[j]() > 0.5:
        parts_in_stock = [model.x[i,j]() for i in model.parts]
        print(f"Stock {j+1}: used, parts = {parts_in_stock}")

print("\n----- Total Profit -----")
print(model.profit())
