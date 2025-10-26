import csv

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
                current_parts.append((length, width, cost))

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
    problems = read_csp_file()
    for i, (parts, stock) in enumerate(problems, start=1):
        print(f"\nProblem {i}:")
        print(f" Stock size: {stock}")
        print(" Parts (L, W, C):")
        for p in parts:
            print("  ", p)

if __name__ == "__main__":
    main()