
import numpy as np
import sys
import os
import time
import random

sys.path.append(os.path.abspath("Ass5"))
from assignment5 import Assignment5
from functionUtils import AbstractShape

def noisy_circle(cx=0, cy=0, radius=1, noise=0.1):
    def sample():
        theta = random.uniform(0, 2*np.pi)
        r = radius + random.uniform(-noise, noise)
        return (cx + r*np.cos(theta), cy + r*np.sin(theta))
    return sample

def verify_fit():
    print("=== Verifying Assignment 5: Fit Shape ===")
    ass5 = Assignment5()
    
    # Test 1: Unit Circle Fit
    print("Test 1: Noisy Circle (R=1, Noise=0.1)")
    sampler = noisy_circle(1, 1, 1, 0.1) # Center (1,1)
    
    start = time.time()
    shape = ass5.fit_shape(sampler, maxtime=5) # 5 sec budget
    elapsed = time.time() - start
    
    # Calculate Area of fitted shape
    area_fitted = shape.area() # Using default area method from AbstractShape/MyShape if implemented?
    # AbstractShape.area() is usually not implemented, but Ass5.area() is.
    # The assignment says "return an object which extends AbstractShape... error of the area function of the shape".
    # Wait, does MyShape need to implement .area()? 
    # The grading policy says "grade is affected by the error of the area function of the shape returned".
    # AbstractShape generally implies user might need to implement area there or the grader uses Ass5.area(shape.contour).
    # Let's check Ass5.area(shape.contour).
    
    print(f"Fit Time: {elapsed:.4f}s (Budget: 5s)")
    
    # Check Area Accuracy
    # Note: Using Ass5.area to measure the area of the shape we just created
    computed_area = ass5.area(shape.contour)
    expected_area = np.pi
    error = abs(computed_area - expected_area)
    
    print(f"Fitted Area: {computed_area:.4f} (Expected {expected_area:.4f})")
    print(f"Error: {error:.4f} -> {'PASS' if error < 0.1 else 'FAIL'}")

    # Test 2: Verify Contour Points
    pts = shape.contour(10)
    print(f"Contour(10) returns {len(pts)} points.")
    
    if elapsed > 5.5: 
        print("FAIL: Time Limit Exceeded")
    else:
        print("PASS: Time Check")

    # Test 3: Non-Star-Convex Shape (e.g. C-Shape or Thin Rectangle)
    # Generic "U" shape of points
    print("\nTest 3: U-Shape (Non-Star-Convex)")
    def u_shape_sample():
        # U shape: Left | Bottom | Right
        # x from -1 to 1. y from 0 to 2.
        # Randomly choose segment
        seg = random.choice([0, 1, 2])
        if seg == 0: # Left: x=-1, y in [0,2]
            return (-1 + random.gauss(0, 0.05), random.uniform(0, 2))
        elif seg == 1: # Bottom: x in [-1, 1], y=0
            return (random.uniform(-1, 1), 0 + random.gauss(0, 0.05))
        else: # Right: x=1, y in [0,2]
            return (1 + random.gauss(0, 0.05), random.uniform(0, 2))
            
    # Area of U-shape (conceptually 0 width, but effectively fitting a curve)
    # Ideally should fit the U. Using simplified area check is hard.
    # Let's just check if it crashes or produces huge bounds.
    
    try:
        shape_u = ass5.fit_shape(u_shape_sample, maxtime=5)
        area_u = ass5.area(shape_u.contour)
        print(f"U-Shape Area: {area_u:.4f} (Should be small/reasonable, NOT millions)")
        if area_u > 100: print("FAIL: Massive Area (Sorting Artifact?)")
        else: print("PASS: Reasonable Area")
    except Exception as e:
        print(f"FAIL: Crashed - {e}")

if __name__ == "__main__":
    verify_fit()
