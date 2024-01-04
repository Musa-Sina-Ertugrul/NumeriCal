import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from sympy import Function,Symbol
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sym_expr import SymPyExpression
from sympy.parsing.latex import parse_latex
from scipy.optimize import minimize

def fixed_point_method(func_repr : str, x0 : float, max_iter : int =100, tolerance : float=1e-6):
    """
    Find the root of a function using the fixed-point method.

    Parameters:
    - func_repr: str
    - x0: Initial guess
    - max_iter: Maximum number of iterations
    - tolerance: Tolerance for error

    Returns:
    - roots: Computed roots at each iteration
    - iterations: Number of iterations performed
    """
    result : list = []
    iterations : int = 0
    g_x = parse_expr(func_repr + "+ x")
    while max_iter > iterations:
        if x0 > -tolerance and x0 < tolerance:
            break
        x_new : float = g_x.evalf(subs={"x": x0})
        if x0 == x_new:
            break
        x0 = x_new
        result.append(x0)
        print(x0)
        iterations += 1
        
    return result, iterations

    # Plotting code
    plt.figure(figsize=(8, 6))
    plt.plot(range(len(roots)), roots, 'ro-', label='Root at each iteration')
    plt.xlabel('Iteration')
    plt.ylabel('Root')
    plt.title('Fixed-Point Method')
    plt.legend()
    plt.show()

    return roots, iterations

def plot_convergence(iterations, roots, true_root=None, title='Convergence Plot'):
    """
    Plot the convergence of the fixed-point method.

    Parameters:
    - iterations: Number of iterations performed
    - roots: Computed roots at each iteration
    - true_root: True root value for reference (if available)
    - title: Plot title
    """
    fig, ax = plt.subplots()
    ax.plot(range(len(roots)), roots)
    if true_root is not None:
        ax.axhline(true_root, color='r', linestyle='--')
        ax.set_title(title)
        ax.set_ylabel('Approximation')
        ax.set_xlabel('Iteration')

    else:
        ax.set_title(title + ' (No known true root)')
        ax.set_ylabel('Approximation')
        ax.set_xlabel('Iteration')
        ax2 = ax.twinx()
        ax2.plot(range(len(iterations)), iterations, 'b--')
        ax2.set_ylabel('# Iterations')
        plt.show()
    




# Function to find the root of
def f(x):
    return x**3 - 3*x

# Initial guess
x0 = 1.5

# Find the root using the fixed-point method
roots, iterations = fixed_point_method("x**3.0 - 3.0*x", x0)

print(f"Root: {roots[-1]}")
print(f"Iterations: {iterations}")