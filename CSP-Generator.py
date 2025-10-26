import csv
import random


def main():
    with open("csp_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        problem_qty=random.randint(5,15)
        # problem_qty=2
        print(f"Generating {problem_qty-1} problems")
        for problem in range(1,problem_qty): # Diffrent Problems
            var_qty=random.randint(3,15)
            print(f"Generating problem with {var_qty-1} variables")

            writer.writerow(["Problem" + str(problem)])

            for variable in range(1,var_qty): #Variables in problems
                row = [
                    "Part"+ str(variable),
                    random.randint(1, 40), #Part Length
                    random.randint(1, 40), #Part Width
                    random.randint(1, 20)  #Part Cost
                ]
                writer.writerow(row)

            row = [
                    "stock",
                    random.randint(1, 500), #Stock Length
                    random.randint(1, 500)  #Stock Width
                ]
            writer.writerow(row)

        print("Generation Complete")


if __name__ == "__main__":
    main()
