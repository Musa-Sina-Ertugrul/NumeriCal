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
)
from sympy.parsing.sympy_parser import parse_expr
from sympy.polys.polyerrors import PolynomialError


def take_diff(expr):
    x = Symbol("x")
    return diff(expr, x), x


def find_extremums(expr) -> list:
    first_derivative, x = take_diff(expr)
    try:
        extremums: list = sorted(nroots(first_derivative, n=6))
        return extremums
    except PolynomialError:
        return [float(first_derivative)]


def find_lims(expr, extremums: list, tolerance: float = 1e-6) -> list:
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
    signs = [
        "+"
        if e2 > e and e2 > 0
        else "-"
        if e2 > e and e2 < 0
        else "+"
        if e2 < e and e2 < 0
        else "-"
        for e, e2 in lims[:-1]
    ]
    signs.append(
        *[
            "+"
            if e2 > e and e2 > 0
            else "+"
            if e2 > e and e2 < 0
            else "-"
            if e2 < e and e2 < 0
            else "+"
            for e, e2 in lims[-1:]
        ]
    )
    return signs


def make_expression(func_repr: str) -> object:
    return parse_expr(func_repr)


def find_extremums_first_diff(expr) -> list:
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
    directions = ["u" if (e2 - e) < 0 else "d" for e2, e in lims]
    return directions


def check_opposite_sign(signs: list) -> bool:
    match signs[0]:
        case "+":
            return "-" in set(signs[1:])
        case "-":
            return "+" in set(signs[1:])
        case _:
            raise NoAssumption("Wrong Sign")


def check_opposite_direction(directions: list):
    if directions != []:
        match directions[0]:
            case "u":
                return "d" in set(directions[1:])
            case "d":
                return "u" in set(directions[1:])
            case _:
                raise NoAssumption("Wrong Sign")
    return True


def make_assumption(extremums: list, directions: list, signs: list) -> list:
    points = []
    if all([True if sign == "+" else False for sign in signs]) or all(
        [True if sign == "-" else False for sign in signs]
    ):
        return points
    for i, extremum in enumerate(extremums):
        if check_opposite_direction(directions[i:]) and check_opposite_sign(signs[i:]):
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

    while max_iter > 0 and error_1 > tolerance and error_2 > tolerance:
        x_new: float = g_x.evalf(subs={"y": x0}).rhs
        error_1 = abs(x_new - x0)
        error_2 = abs(expr.evalf(subs={"x": x_new}))
        result.append(x0)
        x0 = x_new
        max_iter -= 1

    return result

class NoAssumption(RuntimeError):
    pass

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
        super().__init__(target=target, args=args)
        self.result = None
        self.target: callable = target
        self.args: Iterable[Any] = args

    def run(self) -> None:
        self.result = self.target(*self.args)


def make_g_x(expr):
    x = Symbol("x")
    y = Symbol("y")
    eq = Eq(expr, y)
    result: list = []
    for solved_eq in solve(eq, x):
        result.append(Eq(x, solved_eq))
    return result


def make_func_imgs(expr, g_x: list) -> None:
    for i, g in enumerate(g_x):
        with open(f"g_x_{str(i)}.png", "wb") as outputfile:
            preview(g, viewer="BytesIO", outputbuffer=outputfile)

    with open(f"f_x.png", "wb") as outputfile:
        preview(expr, viewer="BytesIO", outputbuffer=outputfile)


def main(func_repr: str, max_iter: int = 500, tolerance: float = 1e-6):
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
    assumptions = assumptions if assumptions != [] else extremums
    if assumptions == []:
        raise NoAssumption("Starting point did not be found, Use different function")
    dicts_1: list = [
        {
            "target": fixed_point_method,
            "args": (expr, g, assumption - 2*tolerance, max_iter, tolerance),
        }
        for assumption in assumptions
        for g in g_x
    ]
    dicts_2: list = [
        {
            "target": fixed_point_method,
            "args": (expr, g, assumption + 2*tolerance, max_iter, tolerance),
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

    #make_func_imgs(expr, g_x)

    return results


if __name__ == "__main__":
    init_printing(use_latex="mathjax")
    # Find the root using the fixed-point method
    print(main("x**2 - 2"))