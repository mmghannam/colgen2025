from typing import List
from pyscipopt import Model, quicksum

def binpacking_compact(sizes: List[int], capacity: int) -> Model:
    model = Model("Binpacking")
    
    # TODO: Implement the compact bin packing formulation

    return model