A Python Interface to Conic Optimization Solvers
================================================

PICOS is a user friendly Python API to several conic and integer programming
solvers, very much like [YALMIP](http://users.isy.liu.se/johanl/yalmip/) or
[CVX](http://cvxr.com/cvx/) under [MATLAB](http://www.mathworks.com/).

PICOS allows you to enter a mathematical optimization problem as a **high level
model**, with painless support for **(complex) vector and matrix variables** and
**multidemensional algebra**. Your model will be transformed to the standard form
understood by an appropriate solver that is available at runtime. This makes
your application **portable** as users have the choice between several commercial
and open source solvers.

Features
--------

PICOS runs under both **Python 2** and **Python 3** and supports the following solvers
and problem types:

| Solver | Interface | [LP](https://en.wikipedia.org/wiki/Linear_programming) | [SOCP](https://en.wikipedia.org/wiki/Second-order_cone_programming) | [SDP](https://en.wikipedia.org/wiki/Semidefinite_programming) | [QP](https://en.wikipedia.org/wiki/Quadratic_programming) | [QCQP](https://en.wikipedia.org/wiki/Quadratically_constrained_quadratic_program) | [GP](https://en.wikipedia.org/wiki/Geometric_programming) | [EXP](https://docs.mosek.com/modeling-cookbook/expo.html) | [MIP](https://en.wikipedia.org/wiki/Integer_programming) | License | Note |
| --------------------------------------------------------- | ---------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | ----------------------------------------------------- |
| [CPLEX](https://www.ibm.com/analytics/cplex-optimizer)    | included                                                   | Yes | Yes |     | Yes | Yes |     |     | Yes | Commercial    |                                                       |
| [CVXOPT](https://cvxopt.org/)                             | not needed                                                 | Yes | Yes | Yes | Yes | Yes | Yes |     |     | Open Source   |                                                       |
| [ECOS](https://www.embotech.com/ECOS)                     | [ecos-python](https://github.com/embotech/ecos-python)     | Yes | Yes |     | Yes | Yes | Yes | Yes | Yes | Open Source   | [WIP](https://gitlab.com/picos-api/picos/tree/future) |
| [GLPK](https://www.gnu.org/software/glpk/)                | [swiglpk](https://github.com/biosustain/swiglpk)           | Yes |     |     |     |     |     |     | Yes | Open Source   | [WIP](https://gitlab.com/picos-api/picos/tree/future) |
| [Gurobi](http://www.gurobi.com/products/gurobi-optimizer) | included                                                   | Yes | Yes |     | Yes | Yes |     |     | Yes | Commercial    |                                                       |
| [MOSEK](https://www.mosek.com/)                           | included                                                   | Yes | Yes | Yes | Yes | Yes |     |     | Yes | Commercial    |                                                       |
| [SMCP](http://smcp.readthedocs.io/en/latest/)             | not needed                                                 | Yes | Yes | Yes | Yes | Yes |     |     |     | Open Source   |                                                       |
| [SCIP](http://scip.zib.de/)                               | [PySCIPOpt](https://github.com/SCIP-Interfaces/PySCIPOpt/) | Yes | Yes |     | Yes | Yes |     |     | Yes | Noncommercial | [WIP](https://gitlab.com/picos-api/picos/tree/future) |

To use a solver, you need to seperately install it along with the (low-level) Python interface listed here.

### Example

This is what it looks like to solve a multidimensional mixed integer program
with PICOS:

```python
>>> import picos
>>> P = picos.Problem()
>>> x = P.add_variable("x", 2, vtype="integer")
>>> C = P.add_constraint(x <= 5.5)
>>> P.set_objective("max", 1|x) # 1|x is the sum over x
>>> solution = P.solve(verbose = 0)
>>> print(solution["status"])
'integer optimal solution'
>>> print(P.obj_value())
10.0
>>> print(x)
[ 5.00e+00]
[ 5.00e+00]
>>> print(C.slack)
[ 5.00e-01]
[ 5.00e-01]
```

### Documentation

The full documentation can be found [here](https://picos-api.gitlab.io/picos/).

Installation
------------

### Via pip

If you are using [pip](https://pypi.org/project/pip/) you can run
``pip install picos`` to get the latest release.

### Via Anaconda

If you are using [Anaconda](https://anaconda.org/) you can run
``conda install -c picos picos`` to get the latest release.

### Via your system's package manager

On **Arch Linux**, there are seperate packages in the AUR for
[Python 2](https://aur.archlinux.org/packages/python2-picos/) and
[Python 3](https://aur.archlinux.org/packages/python-picos/).

### From source

If you are installing PICOS manually, you can choose between a number of
[development versions](https://gitlab.com/picos-api/picos/branches) and
[source releases](https://gitlab.com/picos-api/picos/tags).
You will need to have at least the following Python packages installed:

- [Six](https://pypi.org/project/six/)
- [NumPy](http://www.numpy.org/)
- [CVXOPT](https://cvxopt.org/)

Credits
-------

### Developers

- [Guillaume Sagnol](http://page.math.tu-berlin.de/~sagnol/) is PICOS' initial
  author and primary developer since 2012.
- [Maximilian Stahlberg](about:blank) is extending and maintaining PICOS since
  2017.

### Contributors

For an up-to-date list of all code contributors, please refer to the
[contributors page](https://gitlab.com/picos-api/picos/graphs/master).
Should a reference from before 2019 be unclear, you can refer to the
[old contributors page](https://github.com/gsagnol/picos/graphs/contributors)
on GitHub as well.

### License

PICOS is free and open source software and available to you under the terms of
the [GNU GPL v3](https://gitlab.com/picos-api/picos/blob/master/LICENSE.txt).
