"""
In this assignment you should interpolate the given function.
"""

import numpy as np
import time
import random


class Assignment1:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        starting to interpolate arbitrary functions.
        """
        self.cache = {}

    def interpolate(self, f: callable, a: float, b: float, n: int) -> callable:
        """
        Interpolate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the interpolation error.
        Your secondary objective is minimizing the running time. 
        The assignment will be tested on variety of different functions with 
        large n values. 
        
        Interpolation error will be measured as the average absolute error at 
        2*n random points between a and b. See test_with_poly() below. 

        Note: It is forbidden to call f more than n times. 

        Note: This assignment can be solved trivially with running time O(n^2)
        or it can be solved with running time of O(n) with some preprocessing.
        **Accurate O(n) solutions will receive higher grades.** 
        
        Note: sometimes you can get very accurate solutions with only few points, 
        significantly less than n. 
        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        n : int
            maximal number of points to use.

        Returns
        -------
        The interpolating function.
        """
        
        if n == 1:
            return lambda x: f((a + b) / 2)

        def get_cheb_canonical(N):
            # Check cache first
            if N in self.cache:
                return self.cache[N]
                
            if N == 1:
                return np.array([0.0]), np.array([1.0])

            # Chebyshev nodes of the second kind (Extrema) in [-1, 1]
            j = np.arange(N)
            z = np.cos(j * np.pi / (N - 1))
            
            # Barycentric Weights (Chebyshev 2nd kind)
            weights = np.ones(N)
            weights[0] = 0.5
            weights[N - 1] = 0.5
            weights[1::2] = -1 * weights[1::2]
            
            self.cache[N] = (z, weights)
            return z, weights

        # Attempt to use n points with vectorization
        z_nodes, weights = get_cheb_canonical(n)
        
        # Map z from [-1, 1] to [a, b]
        nodes = (b - a) / 2 * z_nodes + (a + b) / 2
        
        used_n = n
        
        try:
            # Vectorization attempt (consumes 1 invocation)
            res = f(nodes)
            
            # Verify result format
            if np.isscalar(res):
                y_values = np.full(n, res)
            elif np.shape(res) == (n,):
                y_values = np.array(res)
            else:
                raise ValueError("Shape mismatch or invalid return")
                
        except Exception:
            # Fallback: Vectorization failed. We used 1 invocation.
            # We must proceed with n-1 points to stay within budget.
            used_n = n - 1
            if used_n < 1:
               # Should only happen if input n=1 (handled) or n=1 failed?
               # If input n=2 -> used_n=1.
               pass
            
            # Recompute nodes/weights for n-1
            z_nodes_fallback, weights_fallback = get_cheb_canonical(used_n)
            nodes = (b - a) / 2 * z_nodes_fallback + (a + b) / 2
            weights = weights_fallback
            
            y_values = np.zeros(used_n)
            for i in range(used_n):
                y_values[i] = f(nodes[i])

        self.nodes = nodes
        self.y_values = y_values
        self.weights = weights

        def result(x):
            diff = x - nodes
            
            # Check for exact node match
            close_mask = np.abs(diff) < 1e-14
            if np.any(close_mask):
                return y_values[np.argmax(close_mask)]
            
            t = weights / diff
            numerator = np.dot(t, y_values)
            denominator = np.sum(t)
            
            # Avoid division by zero in rare cases outside interval (shouldn't happen with Cheb 2nd)
            if denominator == 0:
                return 0 # Or closest node
                
            return numerator / denominator

        return result


##########################################################################


import unittest
from functionUtils import *
# from tqdm import tqdm


class TestAssignment1(unittest.TestCase):

    def test_with_poly(self):
        T = time.time()

        ass1 = Assignment1()
        mean_err = 0

        d = 30
        for i in range(100):
            a = np.random.randn(d)

            f = np.poly1d(a)

            ff = ass1.interpolate(f, -10, 10, 100)

            xs = np.random.random(200)
            err = 0
            for x in xs:
                yy = ff(x)
                y = f(x)
                err += abs(y - yy)

            err = err / 200
            mean_err += err
        mean_err = mean_err / 100

        T = time.time() - T
        print(T)
        print(mean_err)

    def test_with_poly_restrict(self):
        ass1 = Assignment1()
        a = np.random.randn(5)
        f = RESTRICT_INVOCATIONS(10)(np.poly1d(a))
        ff = ass1.interpolate(f, -10, 10, 10)
        xs = np.random.random(20)
        for x in xs:
            yy = ff(x)

if __name__ == "__main__":
    unittest.main()
