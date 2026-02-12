
import numpy as np
import sys
import os
import math

# Path
sys.path.append(os.path.abspath("Ass5"))
from assignment5 import Assignment5

def verify_area():
    ass5 = Assignment5()
    print("=== Verifying Assignment 5: Area ===")
    
    # 1. Unit Square
    # Points: (0,0), (1,0), (1,1), (0,1)
    # Area = 1
    def square_contour(n):
        # Generate n points on square perimeter
        # This is surprisingly tricky to generate uniformly spaced points for general n
        # But for the assignment, we assume contour(n) provides roughly equal spacing.
        # Let's just simulate returning the vertices + points on edges.
        pts = []
        # Simple parameterization by perimeter
        perimeter = 4.0
        step = perimeter / n
        for i in range(n):
            t = i * step
            if t < 1: pts.append((t, 0)) # Bottom
            elif t < 2: pts.append((1, t-1)) # Right
            elif t < 3: pts.append((1-(t-2), 1)) # Top
            else: pts.append((0, 1-(t-3))) # Left
        return pts
        
    area_sq = ass5.area(square_contour, maxerr=0.001)
    print(f"Square Area: {area_sq:.6f} (Expected 1.0) -> {'PASS' if abs(area_sq - 1.0) < 0.001 else 'FAIL'}")

    # 2. Unit Circle
    # Area = pi ~ 3.14159
    def circle_contour(n):
        theta = np.linspace(0, 2*np.pi, n, endpoint=False)
        return list(zip(np.cos(theta), np.sin(theta)))
        
    area_circ = ass5.area(circle_contour, maxerr=0.001)
    print(f"Circle Area: {area_circ:.6f} (Expected {np.pi:.6f}) -> {'PASS' if abs(area_circ - np.pi) < 0.001 else 'FAIL'}")
    
    # 3. Time Check
    import time
    start = time.time()
    for _ in range(10):
        ass5.area(circle_contour, maxerr=1e-5)
    t = (time.time() - start) / 10
    print(f"Avg Time (Circle High Prec): {t:.5f} sec")

if __name__ == "__main__":
    verify_area()
