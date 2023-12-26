import numpy as np
import json



class Fixed_Point:
    def __init__(self,expression,initial_guess,tolerance,max_iterations):
        """
        Initializes the Fixed_Point class.

        Parameters:
            expression (function): The original function f(x) for which we want to find the root.
            initial_guess (float): Initial guess for the root.
            tolerance (float): Tolerance, a small value to stop iterations.
            max_iterations (int): Maximum number of iterations.
        """
        self.expression = expression
        self.initial_guess = initial_guess
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def transform_function(self,x):
        """
        Transforms the original function f(x) into the equivalent form x = g(x).

        Parameters:
            x (float): Input value.

        Returns:
            float: Transformed value.
        """
        # Replace this with your specific transformation
        return NotImplementedError
    
    def find_root(self):
        """
        Finds a root of the original function using the Fixed-Point Iteration Method.

        Returns:
            float: Approximation of the root.
            int: Number of iterations performed.
        """
        return NotImplementedError



def test():
    expression = input("Enter the function f(x): ")
    x_0 = input("Enter the initial guess x_0: ")
    tol = input("Enter the tolerance (e.g., 1e-6): ")
    max_iter = input("Enter the maximum number of iterations: ")
    Fixed_Point(expression,x_0,tol,max_iter)

if __name__== '__main__':
    test()