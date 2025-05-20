<p align="center">
  <img src="https://github.com/user-attachments/assets/9d9f91fe-2e1a-4d95-aac5-bea1cb643975" alt="image"/>
</p>

Hello, and welcome to the practical session of the Column Generation School 2025 👋 

### Before you start
You will need PySCIPOpt in order to complete the exercises. If you haven't already, the easiest way to install it is via pip. 
You will also need `pytest` to run the tests. You can run a specific test with `pytest <test_name>`.
To install them, run this in your terminal:
```bash
pip install pyscipopt pytest
```

Note that some Ubuntu versions do not allow you to install pip packages globally. The proper way to use it is to create a virtual environment, activate it, and then install the packages in there with the following commands:

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pyscipopt pytest
```

For additional installation options, we direct you to the PySCIPOpt repo: [INSTALL.md](https://github.com/scipopt/PySCIPOpt/blob/master/INSTALL.md) 

### Session Structure
This session is organized in a series of exercises that will guide you towards implementing your own Branch-and-Price solver for the bin packing problem. After this, some bonus exercises give you the extra challenge of adding various speedups to the more basic approach.

If you're already familiar with basic modeling in PySCIPOpt, you can go ahead and start going over the [README](bnp/README.md) in the [bnp](bnp) folder. If this is your first time using PySCIPOpt/GurobiPy/XpressPy, then we suggest giving a quick look at either the [intro](intro), and/or the [modeling](modeling) folders. The former goes over model creation, how to add variables and constraints. The latter asks you to implement a knapsack problem, along with some other variants. In both cases, the `README`'s contain information and hints on how to proceed.

Enjoy the workshop, and remember, we’re here if you need help!
