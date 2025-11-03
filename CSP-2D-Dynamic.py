import pyomo.environ as pyomo
import csv


# #Part 1 = 10, Part2 = 20, Part3 = 5, Part4 = 40 
# part1Width=10
# part2Width=20
# part3Width=5
# part4Width=40

# part1length=30
# part2length=20
# part3length=25
# part4length=5

# part1Cost=5
# part2Cost=9
# part3Cost=4
# part4Cost=12

# StockWidth=200
# StockLength=200

def read_csp_file(filename="csp_data.csv"):
    results = []
    current_parts = []
    stock = None

    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue

            # When a new problem begins, store the previous one (if exists)
            if row[0].startswith("Problem"):
                if current_parts:
                    results.append((current_parts, stock))
                current_parts = []
                stock = None

            # Part row
            elif row[0].startswith("Part"):
                length = int(row[1])
                width = int(row[2])
                cost = int(row[3])
                min_constr = int(row[4])
                current_parts.append((length, width, cost,min_constr))

            # Stock row
            elif row[0] == "stock":
                stock_length = int(row[1])
                stock_width = int(row[2])
                stock = (stock_length, stock_width)

        # Append the final problem after the loop ends
        if current_parts:
            results.append((current_parts, stock))

    return results


def main():
    # initialize the model

    problems = read_csp_file()

    for i, (parts, stock) in enumerate(problems, start=1):

        model = pyomo.ConcreteModel()
        
        print(f"\nProblem {i}:") 

        # Define a range of the number of variables
        var_range = pyomo.RangeSet(1,len(parts))

        # Create variables based on the range
        model.x = pyomo.Var(var_range, domain = pyomo.NonNegativeIntegers)

        # Create a constraint list
        model.c = pyomo.ConstraintList()

        current_part = 1
        sumLenght = 0
        sumWidth = 0
        obj=0
        for p in parts:

            model.c.add(model.x[current_part] <= p[3])

            sumLenght+=p[0]*model.x[current_part]
            sumWidth+=p[1]*model.x[current_part]
            obj+=p[2]*model.x[current_part]

            current_part+=1

        stockLenght = stock[0]
        stockWidth = stock[1]
        print(f"stockLenght: {stockLenght}")
        print(f"stockWidth: {stockWidth}")
        print(f"sumLenght is {sumLenght}")
        print(f"sumWidth is {sumWidth}")
        print(f"obj is {obj}")
        model.c.add(sumLenght<=stockLenght)
        model.c.add(sumWidth<=sumWidth)
    
        model.objective = pyomo.Objective(sense = pyomo.maximize, expr = obj)

        # select a solver
        solver = pyomo.SolverFactory('gurobi')

        # solve the problem
        result = solver.solve(model, tee=True)

        print("-----Printing the model-----")
        model.pprint()
        print("-----Printing the results-----")
        print(result)
        for j in model.x:
            print(f"x[{j}] = {model.x[j]():.2f}")
        (f"Objective = {model.objective():.2f}")


if __name__ == "__main__":
    main()
