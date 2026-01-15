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
        
        return r_best if abs(f(r_best)) < maxerr else None

    def _newton_only(self, f: callable, x0: float, maxerr: float) -> float:
        """
        Attempts to find a root starting at x0 using pure Newton-Raphson.
        Used for touching roots where signs don't change.
        """
        MAX_ITER = 20
        MIN_DERIVATIVE = 1e-9
        DERIVATIVE_H = 1e-5

        def df(x):
            return (f(x + DERIVATIVE_H) - f(x - DERIVATIVE_H)) / (2 * DERIVATIVE_H)
            
        current_x = x0
        
        for _ in range(MAX_ITER):
            f_val = f(current_x)
            if abs(f_val) < maxerr:
                return current_x
                
            try:
                d_val = df(current_x)
                if abs(d_val) < MIN_DERIVATIVE:
                    return None
                current_x = current_x - f_val / d_val
            except Exception:
                return None
                
        return None

    def intersections(self, f1: callable, f2: callable, a: float, b: float, maxerr=0.001) -> Iterable:
        """
        Find as many intersection points as you can. 
        """
        # Constants
        N_STEPS = 2000 # Increased for better resolution of close roots
        
        # Define the difference function
        def f(x):
            return f1(x) - f2(x)

        roots = []
        
        # Optimization: Attempt Vectorized Scan first
        step = (b - a) / N_STEPS
        
        try:
            # 1. Generate Grid
            X = np.linspace(a, b, N_STEPS + 1)
            
            # 2. Vectorized Evaluation (Fast)
            Y = f1(X) - f2(X)
            
            # 3. Find Sign Changes (Crossing Roots)
            # sign(Y) returns -1, 0, 1. diff checks adjacent changes.
            # We look for indices where sign changes.
            sign_changes = np.where(np.diff(np.sign(Y)))[0]
            
            for idx in sign_changes:
                x_start = X[idx]
                x_end = X[idx+1]
                root = self._find_root(f, x_start, x_end, maxerr)
                if root is not None:
                    roots.append(root)
                    
            # 4. Find Touching Roots (Local Extrema near zero)
            # Look for points where value is small AND it's a local extremum
            # Logic: |Y| < small_tol AND derivative changes sign (or just local min of |Y|)
            # Simple heuristic: Look for indices where |Y| is exceptionally small
            
            # Filter for small values only to save time
            small_val_indices = np.where(np.abs(Y) < maxerr)[0]
            
            # For each small value, check if it was already found or is a touching root
            # Just feeding these candidates to _newton_only is safe and fast
            for idx in small_val_indices:
                root = self._newton_only(f, X[idx], maxerr)
                if root is not None:
                    roots.append(root)

        except (TypeError, ValueError):
            # Fallback to Scalar Loop if f1/f2 don't support vectorization
            # (e.g. math.sin, if conditions inside lambda)
            x_prev_1 = a
            y_prev_1 = f(a)
            x_prev_2 = None
            y_prev_2 = None
            current_x = a + step
            
            while current_x <= b + step*0.1:
                y_curr = f(current_x)
                
                # Sign Change
                if y_prev_1 * y_curr <= 0:
                    root = self._find_root(f, x_prev_1, current_x, maxerr)
                    if root is not None: roots.append(root)
                
                # Touching Root (Extremum)
                elif x_prev_2 is not None:
                    slope1 = y_prev_1 - y_prev_2
                    slope2 = y_curr - y_prev_1
                    if slope1 * slope2 < 0 and abs(y_prev_1) < maxerr * 10:
                        root = self._newton_only(f, x_prev_1, maxerr)
                        if root is not None: roots.append(root)

                x_prev_2 = x_prev_1
                y_prev_2 = y_prev_1
                x_prev_1 = current_x
                y_prev_1 = y_curr
                current_x += step

        # Filter duplicates and valid range

        if not roots: return []
        
        roots.sort()
        unique_roots = []
        
        # Ensure roots are within [a, b] (Newton might step slightly out)
        valid_roots = [r for r in roots if a - maxerr <= r <= b + maxerr]
        if not valid_roots: return []
        
        unique_roots.append(valid_roots[0])
        for r in valid_roots[1:]:
            if abs(r - unique_roots[-1]) > maxerr:
                unique_roots.append(r)
                
        return unique_roots


##########################################################################


import unittest
from sampleFunctions import *



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
