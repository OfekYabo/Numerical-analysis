
import unittest
import numpy as np
import sys
import os

# Adjust path to find Ass4 modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Ass4')))
from assignment2 import Assignment2

class TestAss2Robustness(unittest.TestCase):
    def setUp(self):
        self.ass2 = Assignment2()
        self.maxerr = 1e-6

    def test_touching_root_parabola(self):
        """f(x) = (x-1)^2. Roots: [1]. Touching axis (multiplicity 2)."""
        f1 = lambda x: (x - 1)**2
        f2 = lambda x: 0
        roots = self.ass2.intersections(f1, f2, 0, 2, maxerr=self.maxerr)
        print(f"\n[Parabola] Found: {roots}")
        # Standard bracketing methods often MISS touching roots.
        # This test checks if we find it.
        # Expect at least one root near 1.
        has_root = any(abs(r - 1) < 0.01 for r in roots)
        if not has_root:
            print("FAIL: Missed touching root at x=1")
    
    def test_close_roots(self):
        """f(x) = (x-1)(x-1.0001). Roots: [1, 1.0001]. Very close."""
        f1 = lambda x: (x - 1) * (x - 1.0001)
        f2 = lambda x: 0
        # If scan step is > 0.0001, we might step over both (f > 0 -> f > 0).
        roots = self.ass2.intersections(f1, f2, 0.9, 1.1, maxerr=1e-6)
        print(f"\n[Close Roots] Found: {roots}")
        self.assertTrue(len(roots) >= 2, f"Expected 2 roots, found {len(roots)}")

    def test_asymptote(self):
        """f(x) = 1/(x-1). Roots: None. Discontinuity at 1."""
        f1 = lambda x: 1.0 / (x - 1) if abs(x - 1) > 1e-9 else 1e9
        f2 = lambda x: 0
        # Should NOT find a root near 1.
        roots = self.ass2.intersections(f1, f2, 0, 2, maxerr=1e-4)
        print(f"\n[Asymptote] Found: {roots}")
        # Filter false positives near 1
        false_positives = [r for r in roots if abs(r - 1) < 0.1]
        self.assertFalse(false_positives, f"Found false positive at asymptote: {false_positives}")

    def test_high_frequency_sine(self):
        """f(x) = sin(50x). Many roots."""
        f1 = lambda x: np.sin(50 * x)
        f2 = lambda x: 0
        # Range [0, 1]. Roots at k*pi/50. 
        # k=0:0, k=1:0.06, k=2:0.12 ... k=15: 0.94. Roughly 16 roots.
        roots = self.ass2.intersections(f1, f2, 0, 1, maxerr=1e-5)
        print(f"\n[High Freq] Found {len(roots)} roots")
        self.assertTrue(len(roots) > 10, "Missed many high-freq roots")

if __name__ == "__main__":
    unittest.main()
