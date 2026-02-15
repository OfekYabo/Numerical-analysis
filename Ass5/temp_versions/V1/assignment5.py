"""
In this assignment you should fit a model function of your choice to data 
that you sample from a contour of given shape. Then you should calculate
the area of that shape. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you know that your iterations may take more 
than 1-2 seconds break out of any optimization loops you have ahead of time.

Note: You are allowed to use any numeric optimization libraries and tools you want
for solving this assignment. 
Note: !!!Despite previous note, using reflection to check for the parameters 
of the sampled function is considered cheating!!! You are only allowed to 
get (x,y) points from the given shape by calling sample(). 
"""

import numpy as np
import time
import random
from functionUtils import AbstractShape



from scipy.interpolate import splprep, splev

class MyShape(AbstractShape):
    def __init__(self, tck):
        # Process coefficients
        self.tck = tck
        
    def area(self):
        # Delegate to Assignment5.area implementation
        return Assignment5().area(self.contour)
        
    def contour(self, n: int):
        # Evaluate spline at n uniformly spaced points in parameter space [0, 1]
        u = np.linspace(0, 1, n, endpoint=False)
        x_rec, y_rec = splev(u, self.tck)
        
        # Zip into (x,y) tuples
        points = list(zip(x_rec, y_rec))
        return points


class Assignment5:
    def __init__(self):
        pass

    def area(self, contour: callable, maxerr=0.001)->np.float32:
        """
        Compute the area of the shape with the given contour. 
        Algorithm: Adaptive Shoelace Formula (Green's Theorem).
        """
        # Start with a reasonable number of points
        n = 100
        MAX_N = 20000 # Safety limit
        
        previous_area = None
        
        while n <= MAX_N:
            # 1. Sample the contour
            points = contour(n) # Returns list/array of (x,y)
            points = np.array(points, dtype=np.float32)
            
            # 2. Extract X and Y
            x = points[:, 0]
            y = points[:, 1]
            
            # 3. Shoelace Formula: 0.5 * |sum(x_i * y_{i+1} - x_{i+1} * y_i)|
            # Efficient vectorized implementation using numpy
            # We wrap around: i+1 for last element is 0
            x_shift = np.roll(x, -1)
            y_shift = np.roll(y, -1)
            
            # Area = 0.5 * abs( sum(x*y_shift) - sum(x_shift*y) )
            current_area = 0.5 * np.abs(np.dot(x, y_shift) - np.dot(x_shift, y))
            
            # 4. Check for convergence
            if previous_area is not None:
                if np.abs(current_area - previous_area) < maxerr:
                    return np.float32(current_area)
            
            previous_area = current_area
            n *= 2
            
        return np.float32(previous_area)
    
    def fit_shape(self, sample: callable, maxtime: float) -> AbstractShape:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape. 
        """
        start_time = time.time()
        samples = []
        
        # 1. Collect Samples
        # Heuristic: spend ~75% of allowed time sampling
        safety_margin = maxtime * 0.75
        
        while (time.time() - start_time) < safety_margin:
            # Collect chunk of samples
            for _ in range(50):
                samples.append(sample())
            
            if len(samples) > 2500: # Enough samples (reduced from 5000 for speed)
                break
                
        pts = np.array(samples)
        if len(pts) < 10: 
             # Return fail-safe circle
             tck, u = splprep([[0, 1, 0, -1], [1, 0, -1, 0]], s=0, per=True)
             return MyShape(tck)
        
        x_pts = pts[:, 0]
        y_pts = pts[:, 1]
        
        # 2. Sort by Nearest Neighbor (TSP Approximation)
        # Robust for non-star-convex shapes
        # Vectorized Nearest Neighbor logic
        
        N = len(pts)
        ordered_indices = np.zeros(N, dtype=int)
        ordered_indices[0] = 0
        
        # Use a boolean mask for unvisited to avoid array resizing
        unvisited_mask = np.ones(N, dtype=bool)
        unvisited_mask[0] = False
        
        current_idx = 0
        
        # Optimization:
        # If N is large, full N^2 is slow.
        # But for N=2500, N^2 = 6.25M.
        # Python loop overhead is meaningful.
        # We can do this slightly faster by batching or just accepting it takes 0.5s.
        
        for i in range(1, N):
            last_pt = pts[current_idx]
            
            # Distances to all points
            # We only care about unvisited.
            # Masking approach:
            
            # Calculate dist squared
            d2 = (pts[:, 0] - last_pt[0])**2 + (pts[:, 1] - last_pt[1])**2
            
            # Set visited dists to infinity
            d2[~unvisited_mask] = np.inf
            
            # Argmin
            next_idx = np.argmin(d2)
            
            ordered_indices[i] = next_idx
            unvisited_mask[next_idx] = False
            current_idx = next_idx
            
        x_ordered = x_pts[ordered_indices]
        y_ordered = y_pts[ordered_indices]
        
        # 3. Spline Fitting (Scipy)
        # s (smoothness factor). 
        # A good guess for s is m * std^2. 
        # We don't know std (noise). Assuming reasonable noise e.g. 10% of scale?
        # Or adaptive s?
        # Let's try s = len(pts) * 0.5 (Heuristic). 
        # If we use too small s, it overfits noise (wiggly).
        # If too large, it smooths out corners.
        # Try a relatively generous smoothing.
        
        # Estimate variance?
        # Adaptive smoothing based on scale.
        # Large shapes (huge extent) -> Relative noise is small -> Interpolation (s=0) is best to avoid shrinkage.
        # Small shapes -> Relative noise is large -> Smoothing (s > 0) is needed to avoid loops.
        
        span = np.max(pts, axis=0) - np.min(pts, axis=0)
        diag = np.linalg.norm(span)
        
        if diag > 50:
            s_val = 0
        else:
            s_val = len(pts) * 0.01
        
        try:
            tck, u = splprep([x_ordered, y_ordered], s=s_val, per=True)
        except Exception:
            # Fallback
            tck, u = splprep([x_ordered, y_ordered], s=0, per=True)
            
        return MyShape(tck)


##########################################################################


import unittest
from sampleFunctions import *



class TestAssignment5(unittest.TestCase):

    def test_return(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=5)
        T = time.time() - T
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertLessEqual(T, 5)

    def test_delay(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)

        def sample():
            time.sleep(7)
            return circ()

        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=sample, maxtime=5)
        T = time.time() - T
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertGreaterEqual(T, 5)

    def test_circle_area(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=30)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)

    def test_bezier_fit(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=30)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)


if __name__ == "__main__":
    unittest.main()
