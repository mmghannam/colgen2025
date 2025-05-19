def test_compact():
    from compact import binpacking_compact
    from generator import random_bin_packing_instance

    number_of_items = [5, 10, 15, 20]
    capacity = 30

    exptected_objectives = [4, 6, 10, 13]

    for (number, expected_objective) in zip(number_of_items, exptected_objectives):
        sizes = random_bin_packing_instance(number, capacity)
        model = binpacking_compact(sizes, capacity)
        model.optimize()
        objective = model.getObjVal()
        assert (objective - expected_objective) < 1e-6, f"Expected {expected_objective}, but got {objective}"
        

if __name__ == "__main__":
    test_compact()
    print("Compact model test passed!")
    