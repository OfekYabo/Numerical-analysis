
import numpy as np
import sys
import os
import time
import random
from scipy.interpolate import splprep, splev

sys.path.append(os.path.abspath("Ass5"))
from assignment5 import Assignment5

def generate_shapes():
    shapes = []
    
    # 1. Noisy Circle (Star-Convex) - The most common case
    def circle_sample():
        theta = random.uniform(0, 2*np.pi)
        r = 1 + random.gauss(0, 0.1) # Noise sigma=0.1
        return (r*np.cos(theta), r*np.sin(theta))
    shapes.append(("Circle", circle_sample, np.pi))
    
    # 2. Noisy U-Shape (Non-Star-Convex)
    def u_shape_sample():
        seg = random.choice([0, 1, 2])
        if seg == 0: return (-1 + random.gauss(0, 0.05), random.uniform(0, 2))
        elif seg == 1: return (random.uniform(-1, 1), 0 + random.gauss(0, 0.05))
        else: return (1 + random.gauss(0, 0.05), random.uniform(0, 2))
    shapes.append(("U-Shape", u_shape_sample, None)) # Area unknown, check topology
    
    # 3. Thin Rectangle (High Aspect Ratio)
    def rect_sample():
        # 10x1 rectangle
        if random.random() < 0.5:
             # Long sides
             x = random.uniform(0, 10)
             y = 0 if random.random() < 0.5 else 1
        else:
             # Short sides
             x = 0 if random.random() < 0.5 else 10
             y = random.uniform(0, 1)
        return (x + random.gauss(0, 0.05), y + random.gauss(0, 0.05))
    shapes.append(("ThinRect", rect_sample, 10.0))
        
    return shapes

def test_area_speed():
    print("\n=== Testing Area Speed/Accuracy ===")
    ass5 = Assignment5()
    
    def complex_contour(n):
        # A flower shape: r = 1 + 0.5*sin(5*theta)
        theta = np.linspace(0, 2*np.pi, n, endpoint=False)
        r = 1 + 0.5 * np.sin(5 * theta)
        return np.column_stack([r*np.cos(theta), r*np.sin(theta)])
    
    # True area of r = 1 + a*sin(k*theta) is pi * (1 + a^2/2)
    expected = np.pi * (1 + 0.5**2 / 2)
    
    start = time.time()
    res = ass5.area(complex_contour, maxerr=1e-3)
    dt = time.time() - start
    err = abs(res - expected)
    print(f"Flower Area: Time={dt:.4f}s, Err={err:.2e}, Val={res:.4f} (Exp {expected:.4f})")

def solve_tsp_2opt(points, maxtime=1.0):
    # 1. Nearest Neighbor Initialization
    N = len(points)
    unvisited = set(range(1, N))
    tour = [0]
    curr = 0
    while unvisited:
        # Simple greedy (slow for logic, fast for now)
        # Vectorized version best
        # For debug, just use simple loop
        min_dist = float('inf')
        nearest = -1
        for cand in unvisited:
            d = (points[curr][0]-points[cand][0])**2 + (points[curr][1]-points[cand][1])**2
            if d < min_dist:
                min_dist = d
                nearest = cand
        tour.append(nearest)
        unvisited.remove(nearest)
        curr = nearest
        
    # 2. 2-Opt Optimization
    # Uncross lines. 
    improved = True
    start_time = time.time()
    while improved and (time.time() - start_time) < maxtime:
        improved = False
        for i in range(1, N - 2):
            for j in range(i + 1, N):
                if j - i == 1: continue # No change
                
                # Check if swap improves distance
                # Dist(i-1, i) + Dist(j, j+1) > Dist(i-1, j) + Dist(i, j+1)
                p1 = points[tour[i-1]]
                p2 = points[tour[i]]
                p3 = points[tour[j]]
                p4 = points[tour[(j+1)%N]]
                
                d_curr = np.sqrt(((p1-p2)**2).sum()) + np.sqrt(((p3-p4)**2).sum())
                d_new = np.sqrt(((p1-p3)**2).sum()) + np.sqrt(((p2-p4)**2).sum())
                
                if d_new < d_curr:
                    tour[i:j+1] = tour[i:j+1][::-1] # Reverse segment
                    improved = True
                    
    return points[tour]

def test_fit_strategies():
    print("\n=== Testing Fit Strategies (2-Opt) ===")
    ass5 = Assignment5()
    
    for name, sampler, exp_area in generate_shapes():
        print(f"--- Shape: {name} ---")
        
        # Collect samples manually to test sorting
        samples = [sampler() for _ in range(1000)]
        pts = np.array(samples)
        
        start = time.time()
        
        # Run 2-Opt
        ordered_pts = solve_tsp_2opt(pts, maxtime=0.5)
        
        # Spline Fit
        tck, u = splprep(ordered_pts.T, s=len(pts)*0.01, per=True)
        # Calculate Area
        # Evaluate spline 
        u_new = np.linspace(0, 1, 1000)
        x_new, y_new = splev(u_new, tck)
        
        # Shoelace
        x = x_new
        y = y_new
        area = 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
        
        dt = time.time() - start
        print(f"  Fitted Area: {area:.4f} (Time: {dt:.4f}s)")
        
        if exp_area:
             err = abs(area - exp_area)
             print(f"  Error: {err:.4f} ({'PASS' if err < 0.2 else 'FAIL'})")
             
        # Path Len
        d = np.sqrt(np.sum(np.diff(ordered_pts, axis=0)**2, axis=1))
        print(f"  Path Len: {np.sum(d):.4f}")

if __name__ == "__main__":
    test_area_speed()
    test_fit_strategies()
