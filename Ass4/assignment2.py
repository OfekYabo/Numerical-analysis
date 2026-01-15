"""
In this assignment you should find the intersection points for two functions.
"""

import numpy as np
import time
import random
from collections.abc import Iterable


class Assignment2:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """
        pass

    def _find_root(self, f: callable, x1: float, x2: float, maxerr: float) -> float:
        """
        Private helper to find a root in the interval [x1, x2] using Hybrid Newton-Bisection.
        Assumes f(x1) * f(x2) <= 0.
        """
        MAX_ITER = 50
        MIN_DERIVATIVE = 1e-9
        DERIVATIVE_H = 1e-5

        def df(x):
            return (f(x + DERIVATIVE_H) - f(x - DERIVATIVE_H)) / (2 * DERIVATIVE_H)

        r_low = x1
        r_high = x2
        r_best = (r_low + r_high) / 2

        for _ in range(MAX_ITER):
            f_val = f(r_best)
            if abs(f_val) < maxerr:
                return r_best

            try:
                d_val = df(r_best)
                if abs(d_val) < MIN_DERIVATIVE:
                    raise ZeroDivisionError

                r_new = r_best - f_val / d_val

                # Check if Newton step is valid (strictly inside current brackets)
                if r_low < r_new < r_high:
                    r_best = r_new
                else:
                    raise ValueError # Fallback
            except (ZeroDivisionError, ValueError):
                # Fallback to Bisection
                r_best = (r_low + r_high) / 2

            # Update brackets
            if f(r_low) * f(r_best) <= 0:
                r_high = r_best
            else:
                r_low = r_best
        
        return None

    def intersections(self, f1: callable, f2: callable, a: float, b: float, maxerr=0.001) -> Iterable:
        """
        Find as many intersection points as you can. 
        """
        # Constants
        N_STEPS = 1000
        SCAN_BUFFER_FACTOR = 10.0

        # Define the difference function
        def f(x):
            return f1(x) - f2(x)

        roots = []
        
        # Optimization: Use a finer grid to catch closely spaced roots.
        step = (b - a) / N_STEPS
        
        if step < maxerr:
            step = maxerr 

        # Pre-calculate first point
        x_prev = a
        y_prev = f(a)
        
        # Scan range
        current_x = x_prev + step
        while current_x <= b + step/SCAN_BUFFER_FACTOR: 
            y_curr = f(current_x)
            
            # Check for sign change
            if y_prev * y_curr <= 0:
                # Root found in [x_prev, current_x]. Refine it.
                # print(f"DEBUG: Calling find_root with f({x_prev})={y_prev}, f({current_x})={y_curr}")
                root = self._find_root(f, x_prev, current_x, maxerr)
                
                # Check if a valid root was found
                if root is not None:
                    # try:
                    #     float(root)
                    # except Exception as e:
                    #     print(f"DEBUG: Root {root} is not float! {e}")
                    roots.append(root)

            # Advance
            x_prev = current_x
            y_prev = y_curr
            current_x += step

        # Filter duplicates
        if not roots: return []
        
        roots.sort()
        unique_roots = []
        unique_roots.append(roots[0])
        for r in roots[1:]:
            if abs(r - unique_roots[-1]) > maxerr:
                unique_roots.append(r)
                
        return unique_roots


##########################################################################


import unittest
from sampleFunctions import *
# from tqdm import tqdm


class TestAssignment2(unittest.TestCase):

    def test_sqr(self):

        ass2 = Assignment2()

        f1 = np.poly1d([-1, 0, 1])
        f2 = np.poly1d([1, 0, -1])

        X = ass2.intersections(f1, f2, -1, 1, maxerr=0.001)

        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))

    def test_poly(self):

        ass2 = Assignment2()

        f1, f2 = randomIntersectingPolynomials(10)

        X = ass2.intersections(f1, f2, -1, 1, maxerr=0.001)

        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))


if __name__ == "__main__":
    unittest.main()
