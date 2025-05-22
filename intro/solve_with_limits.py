def solve_with_limits():
    from pyscipopt import Model, SCIP_PARAMSETTING

    model = Model()

    # TODO: Read the problem roi2alpha3n4.mps.gz

    # TODO: Set the time limit to 20s, the node limit to 15, and a gap limit of 10%

    # TODO: Disable presolving and increase the aggressivness of heuristics
    
    model.optimize()
    
    # TODO: Report which of the limits terminated the solving process, and what the objective value is

    return model