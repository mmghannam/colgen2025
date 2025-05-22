def first_model():
    from pyscipopt import Model

    model = Model()

    # maximize x + y
    # subject to
    #  x + y <= 1
    #  x, y binary

    # TODO: 1. Create variables x and y
    x = model.addVar(vtype="B")
    y = model.addVar(vtype="B")
    
    # TODO: 2. Add the constraint x + y <= 1
    model.addCons(x+y <= 1)

    # TODO: 3. Set the objective function to maximize x + y
    model.setObjective(x+y, "maximize")
    return model

