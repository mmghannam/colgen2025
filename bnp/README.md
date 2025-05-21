## Introduction
Welcome to the practical session of the Column Generation School 2025! We will use the well-known [bin packing problem](https://en.wikipedia.org/wiki/Bin_packing_problem) as an example. Bin packing is a combinatorial optimization problem where a finite number of items of different sizes must be packed into bins or containers each with a fixed capacity. The goal is to minimize the number of bins used. The problem is NP-hard and has many applications in logistics and resource allocation.

The first two sections will give a light overview of bin packing, both its compact and extended formulations. Implementation exercises start in section 3.

If you try to run the branch-and-price code in [`main.py`](main.py), you will encounter errors. This is because some code is missing and must be implemented by you. The error messages tell you what you should do. E.g.: "The knapsack solver is not implemented yet" implies that you should implement the knapsack solver.

> Note: If you're not familiar with modeling languages and PySCIPOpt, you may want to take a look at the [`intro`](../intro/README.md) and the [`modeling`](../modeling/README.md) folders first.

## Section 1. Compact formulation: Modeling with assignments
The bin packing problem is a classic optimization problem that asks:

> How can we pack a set of items with given sizes into the fewest number of bins, without exceeding the capacity of any bin?

Each bin has the same capacity, and the goal is to assign items to bins such that no bin overflows and the total number of bins used is minimized.

Assume an upper bound on the number of bins (e.g., one per item). Let $\mathcal{B}, \, \mathcal{I}$ be the index sets of bins and items, respectively. Then, we can formulate the problem as follows:

$$
\begin{align*}
    \min_{x,y} & \quad \sum_{b \in \mathcal{B}} y_b \quad & \quad & (1) \\
    \textrm{subject to} & \quad \sum_{b \in \mathcal{B}} x_{ib} = 1, \quad & \forall i \in \mathcal{I} \quad & (2)\\
                        & \quad \sum_{i \in \mathcal{I}} s_ix_{ib} \leq Cy_b, \quad & \forall b \in \mathcal{B} \quad & (3)\\
                        & \quad x_{ib} \in \{0,1\}, \quad & \forall i \in \mathcal{I} \, \forall b \in \mathcal{B} \quad & (4)\\
                        & \quad y_b \in \{0,1\}, \quad &\forall b \in \mathcal{B} \quad & (5)
\end{align*}
$$

Variables $y_b$ model whether bin $i$ is used in the solution, and $x_{ib}$ whether item $i$ is packed into bin $b$. Equation (2) ensures that demand is met, Equation (3) that each bin's capacity is not exceeded, and Equation (4) that if a bin is used, then it should be counted in the objective. The objective (1) is the minimization of the $y$ variables, i.e., the number of used bins.
This direct formulation of the bin-packing problem is famously not very good. Some reasons are the enormous amount of symmetry and the subsequent very high sparsity of the constraint matrix.

#### Exercise 0. Implementing the compact formulation

**Your task**: Go to [`compact.py`](compact.py) and implement the formulation for bin packing presented above.

## Section 2. Extended Formulation: Modeling with Packings
Next, we switch our perspective to the so-called "extended" formulation of the bin packing problem. Instead of modeling with assignments of items to bins we *extend* the formulation to look at all possible packings of items into bins. A packing is simply a subset of items that are packed into a bin (respecting its capacity). Using this concept of packings, we arrive at an equivalent formulation.

Given a set of items $I$ and a set of packings $\mathcal{P}$, variable $z_p$ is equal to 1 if packing $p$ is used and 0 otherwise. 

$$
\begin{align*}
\text{minimize}   & \quad \sum_{p \in \mathcal{P}} z_p \quad & \quad & (5) \\
\text{subject to} & \quad \sum_{p \in \mathcal{P}} a_i^{p} z_p = 1, \quad & \forall i \in I \quad & (6) \\
                  & \quad z_p \in \lbrace0, 1\rbrace, \quad & \forall p \in \mathcal{P} \quad & (7) 
\end{align*}
$$

where $\mathcal{P}$ is the set of all possible packings of items into bins.

Constraints (2) ensure that each item is packed into exactly one packing. The objective is to minimize the number of packings (bins) used.

This formulation has one problem. The size of the problem grows exponentially with the number of items. Only instances with a very small number of items can be even loaded in memory. Therefore, we attempt to solve it using a branch-and-price algorithm. This formulation and the general structure required for solving this problem can be found in [bnp.py](bnp.py) (but again, it's missing some code snippets you must add).

## Section 3. Branch-and-Price Algorithm
In this section, we will first discuss how to solve the linear relaxation of the problem using column generation. Then, we will discuss how to handle branching decisions and infeasibility.

### 3.1 Column Generation

Thinking of the exponential number of possible packings, one realizes that most of them are not that useful. For example, if packing 1 corresponds to using item A, and packing 2 to using items A and B, there is no reason to choose packing 1 over 2. Most of the packings are inefficient like this, hinting that only a handful of columns are actually useful. Column generation (which you have been hearing about all week) will find these columns.

Column generation iteratively solves two problems. A Restricted Master Problem (RMP), which is the extended formulation restricted to a very small set of columns, and a pricing problem that generates new columns to add to the RMP. How can it tell which columns to generate? By using the RMP's dual information.

The generic algorithm goes like this:

1. Use a small fixed set of columns to solve the problem
2. Get dual information to find out which type of columns would be beneficial
3. Solve a pricing problem to produce the best column with these characteristics
4. If the reduced cost of this column is negative, add to the columns in 1. and repeat. Otherwise, optimality is achieved.

> Column generation is a method for solving linear programs. Branch and Price is about using Branch and Bound, where the linear relaxation of each node is solved with column generation.

Usually, the column  added to the RMP is the one with the most negative reduced cost, as it is the one that locally improves the solution the most (recall that we are solving an LP). We also need to ensure that the resulting column satisfies the constraints of the compact formulation - it should not exceed the bin capacity. So the column-generating problem should be something the formulation below.

$$
\begin{align*}
\text{minimize} & \quad 1 - \sum_{i \in I} a_i\pi_i \quad & (8) \\
\text{subject to} & \quad \sum_{i \in I} s_i a_i \leq C \quad & (9) \\
& \quad a_i \in \lbrace0, 1\rbrace, \quad \forall i \in I, \quad & (10)
\end{align*}
$$

where $a_i$ is a variable indicating if item $i$ belongs to the packing we are constructing. If we massage the objective function a little, we see that

$\text{minimize} \hspace{0.5em} 1 - \displaystyle\sum_{i \in I} a_i\pi_i = 1 + \text{minimize} - \displaystyle\sum_{i \in I} a_i\pi_i = 1 - \text{maximize} \displaystyle\sum_{i \in I} a_i\pi_i$

 This objective function, allied to Constraint (2), is a knapsack problem. This is very helpful, as it is crucial in column generation to have the ability to quickly generate columns, and knapsack is one of the most well-studied problems in Operations Research, for which there are incredibly efficient algorithms.

 When the objective of the pricing problem is $\geq 0$, the most beneficial packing is not good enough to justify using another bin. And it is at this point that we know we have reached the optimal solution (once more, for the LP).

To reduce the complexity of the code, each of the following exercises is accompanied by a test.
Running the test validates the correctness of the code of this particular exercise.

#### Exercise 1: Pricing

**Your task:** Implement the knapsack pricing problem solver (by implementing a MIP) `solve_knapsack` in [`pricing_knapsack.py`](pricing_knapsack.py).
To check if your implementation is correct, you can run the [`test_pricing_knapsack.py`](test_pricing_knapsack.py) file. Make sure to return a tuple where the first entry is the optimal solution value, and the second is a list containing the indices of the items that were chosen. 

SCIP can handle pricing internally with the `pricer` plugin. You can see the basic infrastructure in [`pricer.py`](pricer.py). The pricer gets the dual information from the RMP (with `getDualsolLinear`), feeds it into the pricing problem (`pricing_solver`), and decides whether to add the resulting column or not (when checking `if min_redcost < 0`). For the curious, you can see more details in [here](https://www.scipopt.org/doc/html/PRICER.php).


### 3.2 Branching

When dealing with compact formulations, solvers tend to have very efficient branching rules. This is sometimes not the case when doing branch-and-price, as the usual variable branching techniques can exhibit strong deficiencies. Suppose we decide to branch on variable $z$. In one of the branches, we add the constraint $z=0$, and in the other $z=1$. This leads to the following:

- $z=1$. We are forcing the resulting RMP to use this specific column, out of a gigantic number of them;
- $z=0$. We are forbidding the resulting RMP to use this specific column, out of a gigantic number of them.

In the first case, the RMP is heavily restricted, and in the second, it is almost not restricted at all. This translates into a very unbalanced tree, which makes the Branch and Bound process incredibly inefficient. Further, in the down branch, it can be very difficult to avoid regenerating the column we just forbade.

The standard way of branching in branch and price for bin packing is the [Ryan-Foster branching](https://www.scipopt.org/doc/html/BINPACKING_BRANCHING.php). The idea is, rather than focusing on a single item, focus on pairs of items. Thus, given two items $i$ and $j$ the two branches look like:

1. Apart: Item $i$ and item $j$ must not appear in the same bin
2. Together: Item $i$ and item $j$ must appear in the same bin

This also splits the problem in two, but in a much more even way.

So, how do we implement this? We first need to find a fractional pair of items.
Let's compute the value of implicit pair variables $r_{ij}$ for all pairs of items $i$ and $j$.
The value of $r_{ij}$ is the sum of the values of all packing variables $z_p$ that contain both items $i$ and $j$.
From this, we can find a fractional pair of items, i.e., a pair of items $i$ and $j$ such that $r_{ij}$ is fractional.

Let us look at the example used in [`test_fractional_pairs`](test_fractional_pairs.py). There are $3$ packings, $a$, $b$, and $c$, each valued at $0.5$ in the optimal LP solution. Packing $a$ contains items $0,1,2$, which means that the pairs of items to consider in this packing are ${(0,1), (0,2), (1,2)}$, and each appears $0.5$ times. Since pair $(1,2)$ otherwise only appears in packing $c$, this pair shows up $0.5+0.5=1$ times, and is thus not a fractional pair. However, since pairs $(0,1)$ and $(0,2)$ appear in all three patterns, they both sum up to $0.5+0.5+0.5=1.5$, a fractional value. So, in this solution, $(0,1)$ and $(0,2)$ are the fractional pairs.

We then use one of these fractional pairs to create the branching constraints. For simplicity, we're choosing the first one. We then create two child nodes, one where the two items in the fractional pair must be together (in the same bin) and one where they must be apart (in different bins). See the diagram below for a visual understanding of this logic, where item pair (yellow, green) was identified as a fractional pair.

<p align="center">
<img src=https://i.imgur.com/lZDxWJO.png />
</p>


#### Exercise 2: Finding Fractional Pairs
**Your task:** Go to `ryan_foster.py` and fill in the missing implementation of the `all_fractional_pairs` function.
This function should return a list of all fractional pairs of items (see above for a definition of a fractional pair).
You can test your implementation by running the [`test_fractional_pairs.py`](test_fractional_pairs.py) file.

#### Exercise 3: Branching
**Your task:** Fill in the missing pieces in [`ryan_foster.py`](ryan_foster.py) (marked with `?`) that save the branching decisions at the child nodes. Recall that the child nodes need to respect the branching decisions of the parent (saved at `parent_together` and `parent_apart`) and add the new pair (`chosen_pair`) either to the together set or to the apart set.

#### Exercise 4: Handling Branching Decisions in Pricing
**Your task:** Enforce the branching decisions in the pricing problem by implementing the `solve_knapsack_with_constraints` function in [`knapsack.py`](knapsack.py). You can start
by copying the `solve_knapsack` function and modifying it by adding the necessary constraints. 
Note that the apart and together constraints don't forbid both items from being absent from the packing.
You can test your implementation by running the [`test_knapsack_with_constraints.py`](test_knapsack_with_constraints.py) file.

The pricing problem does not have information regarding the branching decisions unless explicitly told. Using Ryan-Foster as an example, it might happen that the parent node decided that items $i_1, i_2$ must be kept apart, but the pricing problem does not know this and might generate a packing containing both items. To ensure proper branching, we need to force the prior branching decisions into the pricing problem.


### 3.3 Final step
Now that we have implemented the pricing problem, the branching rule, and handled infeasibility, you have successfully implemented a full branch-and-price algorithm. Congrats!
You can test your implementation by running the [`test_bnp.py`](test_bnp.py) file.

### 3.4 Improving vanilla Branch-and-Price
There are many more tricks to make your Branch-and-Price code faster and more robust. The following is a collection of self-paced exercises that ask you to implement some of these tricks. You may complete them in any order you'd like.

<!-- #### Bonus Exercise: Using integrality
As the objective function of the RMP always takes integer values, you can inform SCIP about it with the [setObjIntegral](https://pyscipopt.readthedocs.io/en/latest/api/model.html#pyscipopt.Model.setObjIntegral) method. In some instances, it might give you a performance improvement.   -->

#### Bonus Exercise: Dual Stabilization

> For this bonus exercise, we suggest using the instance with 200 items and 100 capacity.

Column generation can suffer from convergence issues. One of the most famous is known as the *yo-yo* effect, where the dual values change drastically from one iteration to the other. This is undesirable, since it tends to lead to more pricing iterations.

Your first task is to plot the evolution of the dual values and see their behavior at the root node.

The *yo-yo* effect can be minimized by techniques such as dual stabilization. One way to do this is by smoothing the dual variables. Rather than using the optimal dual values, use a convex combination of these and the optimal dual solution of the previous iteration instead.

For a given $\alpha \in [0,1]$, the smoothed duals $\tilde{\pi}$ can be computed as $\tilde{\pi}_i^t = (1 - \alpha)\pi_i^t + \alpha\tilde{\pi}_i^{t-1}$, where $\pi_i^t$ denotes the dual value of constraint $i$ in the t-th RMP iteration. In the first iteration, $\tilde{\pi} \equiv \pi$.

Experiment around with different $\alpha$'s, notice the impact on the solving and the duals, and settle on one you feel improves the solving process.

> **Note**: It's possible for there to be negative reduced cost columns for the optimal RMP dual values, but not for the stabilized ones. This is called a *misprice*, and requires re-solving the pricing problem with the actual dual values. The conclusion is that we cannot use the stabilized duals for proving optimality.

In comparison with the original run, see the difference in the number of nodes and LP iterations. Compare also both plots. You will likely see a noticeable improvement.

As a little extra bonus exercise, try removing `setObjIntegral` from the master problem. This method tells SCIP that the objective function is always integral, allowing it to round up the dual bounds.

#### Bonus Exercise: Initializing column generation
Column generation requires an initial set of columns to get started. The current implementation starts with the single-item-per-bin solution, which is the worst feasible solution.
Explore different heuristics for bin packing and provide their solutions to the pricer you created.

#### Bonus Exercise: Handling numerics
If you managed to implement everything correctly, try to run your code to solve an instance with 200 items. You will most likely get into an infinite loop. 

Investigate why this happens (the name of the exercise should give you a hint) and fix it. Hint: Look at the reduced cost of the columns you are generating.

#### Bonus Exercise: Speeding up pricing
The current implementation only adds one column per iteration. Implement adding multiple columns per iteration and report how it affects the performance.

Think of simple ways to speed up the pricing rounds. Are there better algorithms for knapsack?

#### Bonus Exercise: Different-sized bins
What is needed to allow for bins of different sizes? Implement it in your Branch-and-Price code.

#### Bonus Exercise: Lagrangian bound
Read about the Lagrangian bound in the context of column generation and implement it in your pricer.
Hint: You can return your computed lower-bound in the pricer, and SCIP will use it to prune the tree.

#### Bonus Exercise: Removing together constraints
Having a constraint stipulating that two items must be packed in the same bin is functionally the same as having a single item with the size of the other two and removing them.
The benefit of doing this instead is that we reduce the size of the pricing problem by one variable and one constraint per together constraint, which might provide a marginal benefit.

Implement this and remember to recover the solution in terms of the original items.
