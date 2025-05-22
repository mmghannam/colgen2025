from typing import List
from pyscipopt import Model, quicksum

def binpacking_compact(sizes: List[int], capacity: int) -> Model:
    model = Model("Binpacking")
    
    # TODO: Implement the compact bin packing formulation
    
    y = {} # y[j] = 1 -> bin j used
    for j in range(len(sizes)):
        y[j] = model.addVar(vtype="B")
    
    x = {} # x[i,j] = 1 -> item i packed into bin j
    for i in range(len(sizes)):
        for j in range(len(sizes)):
            x[i,j] = model.addVar(vtype="B")
        
    # all items packed
    for i in range(len(sizes)):
        model.addCons(sum(x[i,j] for j in range(len(sizes))) == 1)
    
    # capacity not exceeded
    for j in range(len(sizes)):
        model.addCons(sum(sizes[i]*x[i,j] for i in range(len(sizes))) <= y[j]*capacity)

    # minimize number of bins
    model.setObjective(quicksum(y[j] for j in range(len(sizes))))
    model.writeProblem("cgs_demo.cip")

    return model