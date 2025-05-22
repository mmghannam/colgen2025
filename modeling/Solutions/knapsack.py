from pyscipopt import quicksum


def linear_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()
    
    # TODO Implement a linear knapsack, as described in exercise 1
    n_items = len(weights)

    x = {}
    for i in range(n_items):
        x[i] = model.addVar(ub=1)
    
    model.addCons(quicksum(weights[i]*x[i] for i in range(n_items)) <= capacity)
    
    model.setObjective(sum(values[i]*x[i] for i in range(n_items)), "maximize")

    return model

def binary_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()

    # TODO Implement a 0-1 knapsack, as described in exercise 2
    n_items = len(weights)

    x = {}
    for i in range(n_items):
        x[i] = model.addVar(vtype="B")
    
    model.addCons(quicksum(weights[i]*x[i] for i in range(n_items)) <= capacity)
    
    model.setObjective(quicksum(values[i]*x[i] for i in range(n_items)), "maximize")

    return model

def integer_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()

    # TODO Implement an integer knapsack, as described in exercise 3
    n_items = len(weights)

    x = {}
    for i in range(n_items):
        x[i] = model.addVar(vtype="I")
    
    model.addCons(quicksum(weights[i]*x[i] for i in range(n_items)) <= capacity)
    
    model.setObjective(quicksum(values[i]*x[i] for i in range(n_items)), "maximize")

    return model

def limited_knapsack(capacity, weights, values, max_items):
    from pyscipopt import Model
    model = Model()

    # TODO Implement a knapsack limited to 4 items, as described in exercise 4
    n_items = len(weights)

    x = {}
    for i in range(n_items):
        x[i] = model.addVar(vtype="I")
    
    model.addCons(quicksum(weights[i]*x[i] for i in range(n_items)) <= capacity)
    model.addCons(quicksum(x[i] for i in range(n_items)) <= max_items)

    model.setObjective(quicksum(values[i]*x[i] for i in range(n_items)), "maximize")

    return model