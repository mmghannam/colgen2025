Hello, and welcome to the practical session of the Column Generation School 2025! 

> You will need PySCIPOpt in order to complete the exercises. If you haven't already, the easiest way to install it is via pip. Open your terminal and type `pip install pyscipopt`, which installs PySCIPOpt's latest version (at the time of writing, 5.5.0), and numpy (a dependency for matrix operations).

This session is organized in a series of exercises that will guide you towards implementing your own Branch-and-Price solver for the bin packing problem. After these, some self-paced bonus exercises give you the extra challenge of adding various speedups to the more basic approach.

If you're already familiar with basic modeling in PySCIPOpt, you can go ahead and start going over the [`README`](bnp/README.md) in the [bnp](bnp) folder. If this is your first time using PySCIPOpt/GurobiPy/XpressPy, then we suggest giving a quick look at either the [intro](intro), and/or the [modeling](modeling) folders. The former goes over model creation, how to add variables and constraints. The latter asks you to implement a knapsack problem, along with some other variants. In both cases, the `README`'s contain information and hints on how to proceed.

We sincerely hope you enjoy, and don't be afraid to ask for help!