
import unittest
import numpy as np
import sys
import os

# Import the NEW robust implementation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Ass4')))
from assignment2 import Assignment2 as NewAssignment2

class OldAssignment2:
    """
    Recreation of the previous implementation (from file history).
    Used to demonstrate why it fails on touching/close roots.
    """
    def _find_root(self, f, x1, x2, maxerr):
        # Simplified Hybrid Newton from old code for simulation
        r_best = (x1 + x2) / 2
        for _ in range(50):
            if abs(f(r_best)) < maxerr: return r_best
            # (Newton step omitted for brevity, fallback to sign check)
            if f(x1) * f(r_best) <= 0:
                x2 = r_best
            else:
                x1 = r_best
            r_best = (x1 + x2) / 2
        return r_best if abs(f(r_best)) < maxerr else None

    def intersections(self, f1, f2, a, b, maxerr=0.001):
        # OLD LOGIC: Simple sign change detection
        N_STEPS = 1000
        SCAN_BUFFER_FACTOR = 10.0
        def f(x): return f1(x) - f2(x)
        roots = []
        step = (b - a) / N_STEPS
        if step < maxerr: step = maxerr  # The line in question

        x_prev = a
        y_prev = f(a)
        current_x = x_prev + step
        while current_x <= b + step/SCAN_BUFFER_FACTOR:
            y_curr = f(current_x)
            # ONLY checks sign change
            if y_prev * y_curr <= 0:
                root = self._find_root(f, x_prev, current_x, maxerr)
                if root: roots.append(root)
            x_prev = current_x
            y_prev = y_curr
            current_x += step
        return roots

def test_comparison():
    old_impl = OldAssignment2()
    new_impl = NewAssignment2() # The one currently in Ass4/assignment2.py
    
    print("\n=== COMPARISON: Old vs New Implementation ===\n")

    # CASE 1: Touching Root (e.g., (x-1)^2)
    # The curve touches x-axis at 1 but never goes negative.
    print("Test 1: Touching Root (x-1)^2 at x=1")
    f1 = lambda x: (x - 1)**2
    f2 = lambda x: 0
    
    roots_old = old_impl.intersections(f1, f2, 0, 2, maxerr=1e-6)
    roots_new = new_impl.intersections(f1, f2, 0, 2, maxerr=1e-6)
    
    print(f"  Old Found: {len(roots_old)} roots {roots_old}")
    print(f"  New Found: {len(roots_new)} roots {roots_new}")
    if len(roots_new) > len(roots_old):
        print("  -> RESULT: New implementation DETECTED the missing root.")
    else:
        print("  -> RESULT: No improvement.")

    # CASE 2: Close Roots (e.g., (x-1)(x-1.0001))
    # Two roots very close together. Coarse step misses the dip.
    print("\nTest 2: Close Roots at 1.0 and 1.0001")
    f3 = lambda x: (x - 1) * (x - 1.0001)
    
    # Old used small N_STEPS, New uses larger N_STEPS
    roots_old = old_impl.intersections(f3, f2, 0, 2, maxerr=1e-6)
    roots_new = new_impl.intersections(f3, f2, 0, 2, maxerr=1e-6)
    
    print(f"  Old Found: {len(roots_old)} roots")
    print(f"  New Found: {len(roots_new)} roots")
    
    if len(roots_new) == 2 and len(roots_old) < 2:
         print("  -> RESULT: New implementation solved the Resolution issue.")

if __name__ == "__main__":
    test_comparison()
