"""
In this assignment you should find the area enclosed between the two given functions.
The rightmost and the leftmost x values for the integration are the rightmost and 
the leftmost intersection points of the two functions. 

The functions for the numeric answers are specified in MOODLE. 


This assignment is more complicated than Assignment1 and Assignment2 because: 
    1. You should work with float32 precision only (in all calculations) and minimize the floating point errors. 
    2. You have the freedom to choose how to calculate the area between the two functions. 
    3. The functions may intersect multiple times. Here is an example: 
        https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx
    4. Some of the functions are hard to integrate accurately. 
       You should explain why in one of the theoretical questions in MOODLE. 

"""

import numpy as np
import time
import random



class Assignment3:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def integrate(self, f: callable, a: float, b: float, n: int) -> np.float32:
        """
        Integrate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the integration error. 
        Your secondary objective is minimizing the running time. The assignment
        will be tested on variety of different functions. 
        
        Integration error will be measured compared to the actual value of the 
        definite integral. 
        
        Note: It is forbidden to call f more than n times. 
        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the integration range.
        b : float
            end of the integration range.
        n : int
            maximal number of points to use.

        Returns
        -------
        np.float32
            The definite integral of f between a and b
        """
        # Ensure float32 inputs
        a = np.float32(a)
        b = np.float32(b)
        
        # Simpson's rule requires an odd number of points (even number of intervals)
        if n % 2 == 0:
            n -= 1
        
        if n < 3: # Fallback for very small n, though n is usually larger
             n = 3
             
        # Generate points
        x = np.linspace(a, b, n).astype(np.float32)
        h = (b - a) / (n - 1)
        
        # Calculate function values
        y = f(x).astype(np.float32)
        
        # Composite Simpson's Rule: h/3 * (y[0] + 4*sum(odd) + 2*sum(even) + y[n-1])
        # Indices: 0, 1, 2, ..., n-1
        # Odds: 1, 3, ..., n-2
        # Evens: 2, 4, ..., n-3
        
        integral = y[0] + y[-1]
        integral += 4 * np.sum(y[1:-1:2])
        integral += 2 * np.sum(y[2:-1:2])
        
        result = (h / 3) * integral
        
        return np.float32(result)

    def areabetween(self, f1: callable, f2: callable) -> np.float32:
        """
        Finds the area enclosed between two functions. This method finds 
        all intersection points between the two functions to work correctly. 
        
        Example: https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx

        Note, there is no such thing as negative area. 
        
        In order to find the enclosed area the given functions must intersect 
        in at least two points. If the functions do not intersect or intersect 
        in less than two points this function returns NaN.  
        This function may not work correctly if there is infinite number of 
        intersection points. 
        

        Parameters
        ----------
        f1,f2 : callable. These are the given functions

        Returns
        -------
        np.float32
            The area between function and the X axis

        """
        # Dynamic import to handle uncertain project structure
        import sys
        import os
        import traceback # Added for debug
        
        # Try to locate assignment2
        # Prioritize local import
        try:
             from assignment2 import Assignment2
        except ImportError:
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Ass1')))
            try:
                 from assignment2 import Assignment2
            except ImportError:
                 sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Ass3')))
                 from assignment2 import Assignment2

        ass2 = Assignment2()
        
        def difference(x):
            # Handle vectorization (generic inputs)
            if isinstance(x, np.ndarray):
                try:
                    # Try efficient vectorization first
                    return f1(x) - f2(x)
                except (TypeError, ValueError):
                    # Fallback: Function might not support arrays (e.g. math.log)
                    # Process element-wise using the scalar logic below
                    return np.array([difference(xi) for xi in x])

            # Handle scalar inputs (safe evaluation)
            try:
                # Resolve single-element arrays to scalars just in case
                if hasattr(x, 'item'):
                    x = x.item()
                    
                val = f1(x) - f2(x)
                
                if np.isnan(val) or np.isinf(val):
                    return 1e9 
                
                return val
            except (ValueError, ArithmeticError, RuntimeWarning):
                return 1e9 
            except Exception:
                return 1e9

        # Heuristic search range widened to [-100, 100]
        # Pass 'difference' as f1 and 'zero' as f2
        roots = ass2.intersections(difference, lambda x: 0, -100, 100, maxerr=0.001)
        
        if len(roots) < 2:
            return np.float32(np.nan)
            
        roots.sort()
        total_area = np.float32(0.0)
        
        for i in range(len(roots) - 1):
            r_start = roots[i]
            r_end = roots[i+1]
            
            # Integrate the difference function on this segment
            segment_area = self.integrate(difference, r_start, r_end, n=100)
            total_area += np.abs(segment_area)
            
        return total_area


##########################################################################


import unittest
from sampleFunctions import *



class TestAssignment3(unittest.TestCase):

    def test_integrate_float32(self):
        ass3 = Assignment3()
        f1 = np.poly1d([-1, 0, 1])
        r = ass3.integrate(f1, -1, 1, 10)

        self.assertEquals(r.dtype, np.float32)

    def test_integrate_hard_case(self):
        ass3 = Assignment3()
        f1 = strong_oscilations()
        r = ass3.integrate(f1, 0.09, 10, 20)
        true_result = -7.78662 * 10 ** 33
        self.assertGreaterEqual(0.001, abs((r - true_result) / true_result))


if __name__ == "__main__":
    unittest.main()
