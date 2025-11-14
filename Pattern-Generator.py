import csv
import random

def generate_patterns(parts, stock_length, max_patterns=8, max_types_per_pattern=3, min_leftover=10):
    patterns = []
    num_parts = len(parts)

    for p in range(max_patterns):
        pattern = [0] * num_parts

        selected_types = random.sample(range(num_parts), random.randint(1, max_types_per_pattern))

        remaining = stock_length

        for t in selected_types:
            length = parts[t][1]
            max_fit = remaining // length
            if max_fit > 0:
                qty = random.randint(1, max_fit)
                pattern[t] = qty
                remaining -= qty * length

        # Check leftover constraint
        if remaining >= min_leftover:
            patterns.append(pattern)

    return patterns

def main():

    with open("csp_data.csv", "w", newline="") as file:
        writer = csv.writer(file)

        problem_qty = random.randint(2, 5)
        print(f"Generating {problem_qty} problems")

        for problem in range(1, problem_qty + 1):
            writer.writerow([f"Problem{problem}"])
            writer.writerow(["PARTS"])
            writer.writerow(["Part", "Length", "Demand"])

            num_parts = random.randint(3, 6)
            parts = []

            for i in range(1, num_parts + 1):
                length = random.randint(10, 90)
                demand = random.randint(10, 100)
                parts.append((f"Part{i}", length, demand))
                writer.writerow([f"Part{i}", length, demand])

            stock_length = random.choice([100, 200, 300])

            writer.writerow([])
            writer.writerow(["STOCK"])
            writer.writerow(["Length"])
            writer.writerow([stock_length])

            # Generate cutting patterns
            patterns = generate_patterns(parts, stock_length)

            writer.writerow([])
            writer.writerow(["PATTERNS"])
            header = ["Pattern"] + [p[0] for p in parts]
            writer.writerow(header)

            for j, pat in enumerate(patterns, start=1):
                writer.writerow([f"P{j}"] + pat)

    print("Generation Complete")

if __name__ == "__main__":
    main()
