from typing import List
from pyscipopt import Branchrule, SCIP_RESULT


class RyanFoster(Branchrule):
    def __init__(self, *args, **kwargs):
        """
        Branching decisions are stored in a dictionary, where the key is the node number
        and the value is a dictionary with the keys "together" and "apart"
        the value of "together" is a set of pairs of items that must be in the same bin
        the value of "apart" is a set of pairs of items that must be in different bins.
        """
        super().__init__(*args, **kwargs)
        self.branching_decisions = {
            1: {  # root node
                "together": set(),
                "apart": set(),
            }
        }

    def branchexeclp(self, allowaddcons):
        # get the fractional variables from the LP solution
        lpcands, lpcandssol, *_ = self.model.getLPBranchCands()

        patterns_with_vals = [
            (eval(var.name.replace("t_", "")), val) for var, val in zip(lpcands, lpcandssol)
        ]

        chosen_pair = choose_fractional_pair(patterns_with_vals)
        
        # TODO (Exercise 2: choose a fractional pair to branch on)
        # Left subproblem: enforce that pair is in the same bin
        left_node = self.model.createChild(0, 0)
        
        # Getting the current branching decisions
        cur_node_number = self.model.getCurrentNode().getNumber()
        cur_branching_decisions = self.branching_decisions[cur_node_number]

        # Adding the new branching decision to the set of together constraints
        self.branching_decisions[left_node.getNumber()] = {
            "together": cur_branching_decisions["together"].union({chosen_pair}),
            "apart": cur_branching_decisions["apart"]
        }

        # Right subproblem: enforce that pair is in different bins
        right_node = self.model.createChild(0, 0)

        self.branching_decisions[right_node.getNumber()] = {
            "together": cur_branching_decisions["together"],
            "apart": cur_branching_decisions["apart"].union({chosen_pair})
        }
        
        return {"result": SCIP_RESULT.BRANCHED}


def all_fractional_pairs(patterns_with_vals: List[tuple[List[int], float]]) -> List[tuple[int, int]]:
    """
    Find all pairs of items that are fractional in the LP solution

    Parameters:
    patterns_with_vals: List[tuple[List[int], float]] - a list of packings and the value of the variable in the LP solution

    Returns:
    List[tuple[int, int]] - a list of pairs of items that are fractional in the LP solution
    """
    pairs = {}
    for pattern, val in patterns_with_vals:
        for i in range(len(pattern)):
            for j in range(i + 1, len(pattern)):
                if pattern[i] < pattern[j]:
                    tuple = (pattern[i], pattern[j])
                    if tuple not in pairs:
                        pairs[tuple] = val
                    else:
                        pairs[tuple] += val

    return [pair for pair, val in pairs.items() if 1e-6 < val < 1 - 1e-6]


def choose_fractional_pair(patterns_with_vals: List[tuple[List[int], float]]) -> tuple[int, int]:
    """
    Choose a fractional pair to branch on

    Parameters:
    fractional_vars: List[tuple[List[int], float]] - a list of packings and the value of the variable in the LP solution

    Returns:
    tuple[int, int] - the pair of items to branch on
    """

    first_pair = all_fractional_pairs(patterns_with_vals)[0]
    return first_pair