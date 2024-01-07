from threading import Thread
from collections.abc import Callable, Iterable, Mapping
from threading import Thread
from typing import Any
from numba import jit
from sympy import (
    Symbol,
    diff,
    solve,
    nroots,
    solve,
    Eq,
    preview,
    init_printing,
    sympify,
)
from sympy.parsing.sympy_parser import parse_expr
from sympy.polys.polyerrors import PolynomialError


class NoAssumption(RuntimeError):
    """A custom exception class; used when no assumption can be found."""
    pass


class ImeginaryNumber(RuntimeError, TypeError, ValueError):
    """An error class related to imaginary numbers."""
    pass


def take_diff(expr):
    """
    Computes the first derivative of a mathematical expression.

    Args:
    expr (sympy.Basic): The mathematical expression to differentiate.

    Returns:
    tuple: The first derivative and the symbol of the independent variable.
    """
    x = Symbol("x")
    return diff(expr, x), x


def find_extremums(expr) -> list:
    """
    Finds the extremum points of a mathematical expression.

    Args:
    expr (sympy.Basic): The mathematical expression to find extremums.

    Returns:
    list: List of extremum points.
    """
    first_derivative, x = take_diff(expr)
    try:
        extremums: list = sorted(nroots(first_derivative, n=6))
        return extremums
    except PolynomialError:
        return [float(first_derivative)]


def find_lims(expr, extremums: list, tolerance: float = 1e-6) -> list:
    """
    Finds the limits of a mathematical expression at specific points.

    Args:
    expr (sympy.Basic): The mathematical expression to find limits.
    extremums (list): List of points where limits will be calculated.
    tolerance (float): Tolerance for limit calculation.

    Returns:
    list: List of limits at the specified points.
    """
    
    lims: list = [
        (
            expr.evalf(subs={"x": extremum - tolerance}),
            expr.evalf(subs={"x": extremum - 2 * tolerance}),
        )
        for extremum in extremums
    ]
    lims.append(
        (
            expr.evalf(subs={"x": extremums[-1] + tolerance}),
            expr.evalf(subs={"x": extremums[-1] + 2 * tolerance}),
        )
    )
    return lims


def find_signs(lims: list) -> list:
    """
    Determines the signs of a list of limits.

    Args:
    lims (list): List of limits.

    Returns:
    list: List of signs corresponding to the given limits.
    """
    signs = ["-" if e2 > e and e2 > 0 else "-" for e, e2 in lims[:-1]]
    signs.append(*["+" if e2 > e and e2 > 0 else "-" for e, e2 in lims[-1:]])
    return signs


def make_expression(func_repr: str) -> object:
    """
    Creates a symbolic expression from its string representation.

    Args:
    func_repr (str): String representation of the mathematical expression.

    Returns:
    object: The symbolic expression.
    """
    return parse_expr(func_repr)


def find_extremums_first_diff(expr) -> list:
    """
    Finds the extremum points using the second derivative of a mathematical expression.

    Args:
    expr (sympy.Basic): The mathematical expression.

    Returns:
    list: List of extremum points.
    """
    second_derivative, x = take_diff(take_diff(expr)[0])
    try:
        extremums = sorted(nroots(second_derivative, n=6))
        extremums = (
            extremums if extremums != [] else [-second_derivative.evalf(subs={"x": 0})]
        )
        return extremums
    except PolynomialError:
        return [float(second_derivative)]


def find_up_down(lims: list):
    """
    Determines whether the function is increasing or decreasing at specific points.

    Args:
    lims (list): List of limits.

    Returns:
    list: List of directions indicating whether the function is increasing ('u') or decreasing ('d').
    """
    directions = ["u" if (e2 - e) < 0 else "d" for e2, e in lims]
    return directions


def check_opposite_sign(signs: list, extremum: float) -> bool:
    """
    Checks if there is an opposite sign around a given extremum.

    Args:
    signs (list): List of signs.
    extremum (float): The extremum point.

    Returns:
    bool: True if there is an opposite sign, False otherwise.
    """
    match signs[0]:
        case "+":
            return "-" in set(signs[1:]) and extremum > 0
        case "-":
            return "+" in set(signs[1:]) and extremum < 0
    return True


def check_opposite_direction(directions: list, extremum: float):
    """
    Checks if there is an opposite direction around a given extremum.

    Args:
    directions (list): List of directions.
    extremum (float): The extremum point.

    Returns:
    bool: True if there is an opposite direction, False otherwise.
    """
    if directions != []:
        match directions[0]:
            case "u":
                return "d" in set(directions[1:]) and extremum > 0
            case "d":
                return "u" in set(directions[1:]) and extremum < 0
    return True


def make_assumption(extremums: list, directions: list, signs: list) -> list:
    """
    Makes assumptions about potential starting points for fixed-point iterations.

    Args:
    extremums (list): List of extremum points.
    directions (list): List of directions indicating increasing ('u') or decreasing ('d').
    signs (list): List of signs.

    Returns:
    list: List of assumed starting points for fixed-point iterations.
    """
    points = []
    for i, extremum in enumerate(extremums):
        if check_opposite_direction(directions[i:], extremum) and check_opposite_sign(
            signs[i:], extremum
        ):
            points.append(extremum)

    return points


@jit(forceobj=True, nogil=True)
def fixed_point_method(
    expr, g_x, x0: float, max_iter: int = 100, tolerance: float = 1e-6
):
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
    result: list = []
    error_1: float = 1.0
    error_2: float = 1.0
    imag: bool = False
    while max_iter > 0 and error_1 > tolerance * 1000 and error_2 > tolerance * 1000:
        x_new: float = g_x.evalf(subs={"y": x0})
        if not sympify(x_new).is_real:
            imag = True
            break
        error_1 = abs(x_new - x0)
        error_2 = abs(expr.evalf(subs={"x": x_new}))
        result.append(x_new)
        x0 = x_new
        max_iter -= 1
    if imag:
        return fixed_complex_point_iteration(expr, x0, max_iter, tolerance)
    return result


def fixed_complex_point_iteration(
    expr, x0: float, max_iter: int = 100, tolerance: float = 1e-6
) -> list:
    
    """
    Finds the root of a function using the fixed-point method for complex roots.

    Parameters:
    - expr: Mathematical expression representing the function.
    - x0: Initial guess.
    - max_iter: Maximum number of iterations.
    - tolerance: Tolerance for error.

    Returns:
    list: Computed roots at each iteration for complex roots.
    """
    result: list = []
    error_1: float = 1.0
    while max_iter > 0 and error_1 > tolerance * 1000:
        x_new: float = expr.evalf(subs={"x": x0})
        error_1 = abs(x_new)
        result.append(x0)
        x0 = x_new
        max_iter -= 1

    return result


class ReturnThread(Thread):
    def __init__(
        self,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None,
    ) -> None:
        
        """
        A custom thread class that captures the result of the target function.

        Parameters:
        - target: Target function to be executed in the thread.
        - args: Arguments to be passed to the target function.
        """

        super().__init__(target=target, args=args)
        self.result = None
        self.target: callable = target
        self.args: Iterable[Any] = args

    def run(self) -> None:
        """
        Runs the target function in the thread and captures the result.
        """
        self.result = self.target(*self.args)


def make_g_x(expr):
    """
    Generates a list of functions from an expression by solving for the variable.

    Args:
    expr (sympy.Basic): The mathematical expression.

    Returns:
    list: List of functions obtained by solving the expression for the variable.
    """
    x = Symbol("x")
    y = Symbol("y")
    eq = Eq(expr, y)
    result: list = []
    for solved_eq in solve(eq, x):
        result.append(solved_eq)
    return result


def make_func_imgs(expr, g_x: list) -> None:
    """
    Creates images of the mathematical expressions.

    Args:
    expr (sympy.Basic): The original mathematical expression.
    g_x (list): List of expressions representing the fixed-point iteration functions.
    """
    for i, g in enumerate(g_x):
        with open(f"g_x_{str(i)}.png", "wb") as outputfile:
            preview(g, viewer="BytesIO", outputbuffer=outputfile)

    with open(f"f_x.png", "wb") as outputfile:
        preview(expr, viewer="BytesIO", outputbuffer=outputfile)


def main(func_repr: str, max_iter: int = 500, tolerance: float = 1e-6):
    """
    Main function orchestrating the entire process of finding roots using fixed-point iteration.

    Args:
    func_repr (str): String representation of the mathematical expression.
    max_iter (int): Maximum number of iterations.
    tolerance (float): Tolerance for error.

    Returns:
    list: Computed roots using fixed-point iteration.
    """
    expr = make_expression(func_repr=func_repr)
    g_x = make_expression(func_repr=func_repr)
    g_x: list = make_g_x(g_x)
    extremum_first_diff: list = find_extremums_first_diff(expr)
    extremums: list = find_extremums(expr)
    lims: list = find_lims(expr, extremums, tolerance)
    signs: list = find_signs(lims)
    lims_second_diff: list = find_lims(expr, extremum_first_diff, tolerance)
    directions: list = find_up_down(lims_second_diff)
    assumptions: list = make_assumption(extremums, directions, signs)
    if assumptions == []:
        raise NoAssumption("Starting point did not be found, Use different function")
    print(assumptions)
    dicts_1: list = [
        {
            "target": fixed_point_method,
            "args": (expr, g, assumption - 2 * tolerance, max_iter, tolerance),
        }
        for assumption in assumptions
        for g in g_x
    ]
    dicts_2: list = [
        {
            "target": fixed_point_method,
            "args": (expr, g, assumption + 2 * tolerance, max_iter, tolerance),
        }
        for assumption in assumptions
        for g in g_x
    ]
    dicts_1.extend(dicts_2)
    threads: list = [
        ReturnThread(target=dict_["target"], args=dict_["args"]) for dict_ in dicts_1
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    results: list = [thread.result for thread in threads]

    make_func_imgs(expr, g_x)

    if None in results:
        while None in results:
            results.remove(None)

    return results


if __name__ == "__main__":
    init_printing(use_latex="mathjax")
    # Find the root using the fixed-point method
    print(main("x**2 + 2*x + 1"))
