"""
In this assignment you should fit a model function of your choice to data 
that you sample from a given function. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you take an iterative approach and know that 
your iterations may take more than 1-2 seconds break out of any optimization 
loops you have ahead of time.

Note: You are NOT allowed to use any numeric optimization libraries and tools 
for solving this assignment. 

"""

import numpy as np
import time
import random


class Assignment4:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def fit(self, f: callable, a: float, b: float, d:int, maxtime: float) -> callable:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape. 
        
        Parameters
        ----------
        f : callable. 
            A function which returns an approximate (noisy) Y value given X. 
        a: float
            Start of the fitting range
        b: float
            End of the fitting range
        d: int 
            The expected degree of a polynomial matching f
        maxtime : float
            This function returns after at most maxtime seconds. 

        Returns
        -------
        a function:float->float that fits f between a and b
        """

        start_time = time.time()
        
        # --- 1. Custom Linear System Solver ---
        def solve_linear_system(A, b_vec):
            """
            Solves Ax = b using Gaussian Elimination with Partial Pivoting.
            """
            n = len(b_vec)
            Aug = np.hstack([A, b_vec.reshape(-1, 1)]).astype(np.float64)

            for i in range(n):
                pivot_row = i + np.argmax(np.abs(Aug[i:, i]))
                if i != pivot_row:
                    Aug[[i, pivot_row]] = Aug[[pivot_row, i]]
                
                pivot = Aug[i, i]
                if abs(pivot) < 1e-12: continue

                factors = Aug[i+1:, i] / pivot
                Aug[i+1:, i:] -= factors[:, np.newaxis] * Aug[i, i:]

            x = np.zeros(n)
            for i in range(n - 1, -1, -1):
                sum_ax = np.dot(Aug[i, i+1:n], x[i+1:n])
                if abs(Aug[i, i]) > 1e-15:
                    x[i] = (Aug[i, n] - sum_ax) / Aug[i, i]
            
            return x

        # --- 2. Sampling Strategy ---
        t0 = time.time()
        measurement_count = 0
        samples_to_measure = min(d + 5, 50) 
        
        for _ in range(samples_to_measure):
            f(a)
            measurement_count += 1
            if time.time() - t0 > 0.5: 
                break
                
        t_total_measure = time.time() - t0
        t_sample = t_total_measure / measurement_count
        
        remaining = maxtime - (time.time() - start_time)
        budget = max(0.1, remaining - 0.5)
        
        if t_sample > 1e-3:
            estimated_N = int((budget * 0.75) / t_sample)
        elif t_sample > 1e-5:
            estimated_N = int(budget / t_sample)
        else:
             estimated_N = 20000

        N = min(max(estimated_N, 2 * d + 20), 20000) 
        if N < d + 2: N = d + 2

        xs = np.linspace(a, b, N)
        ys = np.array([f(x) for x in xs])

        # --- 3. Normal Equations ---
        m_dim = d + 1
        
        center = (a + b) / 2
        scale = (b - a) / 2
        if scale == 0: scale = 1.0
        
        zs = (xs - center) / scale
        
        z_pows = np.zeros((2 * d + 1, N))
        z_pows[0] = 1.0
        for k in range(1, 2 * d + 1):
            z_pows[k] = z_pows[k-1] * zs
            
        M = np.zeros((m_dim, m_dim))
        v = np.zeros(m_dim)
        
        for i in range(m_dim):
            for j in range(i, m_dim):
                val = np.sum(z_pows[i+j])
                M[i, j] = val
                M[j, i] = val
            v[i] = np.sum(ys * z_pows[i])
            
        # --- 4. Solve ---
        coeffs = solve_linear_system(M, v)
        
        # --- 5. Return Function ---
        def result(x):
            z = (x - center) / scale
            val = 0.0
            p_z = 1.0
            for c in coeffs:
                val += c * p_z
                p_z *= z
            return val

        return result


##########################################################################


import unittest
from sampleFunctions import *


class TestAssignment4(unittest.TestCase):

    def test_return(self):
        f = NOISY(0.01)(poly(1,1,1))
        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertLessEqual(T, 5)

    def test_delay(self):
        f = DELAYED(7)(NOISY(0.01)(poly(1,1,1)))

        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertGreaterEqual(T, 5)

    def test_err(self):
        f = poly(1,1,1)
        nf = NOISY(1)(f)
        ass4 = Assignment4()
        T = time.time()
        ff = ass4.fit(f=nf, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        mse=0
        for x in np.linspace(0,1,1000):            
            self.assertNotEquals(f(x), nf(x))
            mse+= (f(x)-ff(x))**2
        mse = mse/1000

        
        



if __name__ == "__main__":
    unittest.main()
