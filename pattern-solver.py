import pyomo.environ as pyo
import csv
import os


# ============================================================
#  CLEAN + SAFE CSV PARSER FOR YOUR FORMAT
# ============================================================

def read_csp(filename="csp_data.csv"):
    problems = []

    # Read raw CSV rows (may contain empty cells)
    with open(filename, "r") as f:
        raw = list(csv.reader(f))

    # Clean rows — remove empty cells + remove empty rows
    rows = []
    for r in raw:
        cleaned = [c.strip() for c in r if c.strip() != ""]
        if cleaned:
            rows.append(cleaned)

    idx = 0
    n = len(rows)

    # -----------------------------
    #   PARSE EACH PROBLEM BLOCK
    # -----------------------------
    while idx < n:
        row = rows[idx]

        if row[0].startswith("Problem"):
            parts = {}
            patterns = {}
            stock_length = None

            # =======================
            #   READ PARTS SECTION
            # =======================
            while idx < n and rows[idx][0] != "PARTS":
                idx += 1
            idx += 1  # skip PARTS

            # Skip header if present
            if idx < n and rows[idx][0] == "Part":
                idx += 1

            # Read part lines
            while idx < n and rows[idx][0] not in ["STOCK", "PATTERNS"]:
                name = rows[idx][0]

                # robust integer parsing
                try:
                    length = int(rows[idx][1])
                    demand = int(rows[idx][2])
                except:
                    idx += 1
                    continue

                parts[name] = (length, demand)
                idx += 1

            # =======================
            #   READ STOCK SECTION
            # =======================
            while idx < n and rows[idx][0] != "STOCK":
                idx += 1
            idx += 1  # skip STOCK

            # skip "Length" header if present
            if idx < n and rows[idx][0] == "Length":
                idx += 1

            # read stock length
            stock_length = int(rows[idx][0])
            idx += 1

            # =======================
            #   READ PATTERNS SECTION
            # =======================
            while idx < n and rows[idx][0] != "PATTERNS":
                idx += 1
            idx += 1  # skip PATTERNS

            # header row with part names
            header = rows[idx]
            part_names = header[1:]   # skip "Pattern"
            idx += 1

            # Read pattern rows safely
            while idx < n:
                row = rows[idx]

                # stop when new block begins
                if row[0].startswith("Problem"):
                    break
                if row[0] in ["PARTS", "STOCK", "PATTERNS"]:
                    break

                # accept only pattern rows "P1", "P2", etc.
                if not row[0].startswith("P"):
                    idx += 1
                    continue

                # Try to parse integer counts
                try:
                    vals = list(map(int, row[1:]))
                except ValueError:
                    idx += 1
                    continue

                pname = row[0]
                patterns[pname] = dict(zip(part_names, vals))

                idx += 1

            # Store complete problem
            problems.append((parts, stock_length, patterns))

        idx += 1

    return problems


# ============================================================
#   CUTTING STOCK MODEL (Pyomo)
# ============================================================

def solve_cutting_stock(parts, stock_length, patterns):
    model = pyo.ConcreteModel()

    P = list(patterns.keys())
    I = list(parts.keys())

    model.P = pyo.Set(initialize=P)
    model.I = pyo.Set(initialize=I)

    # decision variables
    model.x = pyo.Var(model.P, within=pyo.NonNegativeIntegers)
    model.y = pyo.Var(model.P, within=pyo.Binary)

    # demand constraints
    def demand_rule(m, i):
        return sum(patterns[p][i] * m.x[p] for p in P) >= parts[i][1]
    model.demand = pyo.Constraint(model.I, rule=demand_rule)

    # max +10% overproduction
    def overprod_rule(m, i):
        return sum(patterns[p][i] * m.x[p] for p in P) <= 1.10 * parts[i][1]
    model.overprod = pyo.Constraint(model.I, rule=overprod_rule)

    # linking x ≤ M y
    M = 10000
    def link_rule(m, p):
        return m.x[p] <= M * m.y[p]
    model.link = pyo.Constraint(model.P, rule=link_rule)

    # max patterns used
    Kmax = 8
    model.max_patterns = pyo.Constraint(expr=sum(model.y[p] for p in P) <= Kmax)

    # waste constraint
    total_length_used = sum(
        model.x[p] * sum(patterns[p][i] * parts[i][0] for i in I)
        for p in P
    )
    total_stock_used = stock_length * sum(model.x[p] for p in P)

    waste = total_stock_used - total_length_used
    Wmax = stock_length * 3
    model.waste_constraint = pyo.Constraint(expr=waste <= Wmax)

    # minimize bars used
    model.obj = pyo.Objective(expr=sum(model.x[p] for p in P),
                              sense=pyo.minimize)

    solver = pyo.SolverFactory("gurobi")
    solver.solve(model, tee=False)

    return model


# ============================================================
#   MAIN
# ============================================================

def main():
    problems = read_csp()

    print(os.environ["PATH"])

    for idx, (parts, stock_length, patterns) in enumerate(problems, start=1):
        print(f"\n=== Solving Problem {idx} ===")
        model = solve_cutting_stock(parts, stock_length, patterns)

        for p in model.P:
            if model.x[p]() > 0:
                print(f"{p}: {model.x[p]()} times")

        print(f"Objective (bars used) = {model.obj():.2f}")


if __name__ == "__main__":
    main()
