import unittest
import numpy as np
import sys
import os
import math

# Add Ass4 to path so we can import assignment3
sys.path.append(os.path.abspath('Ass4'))

from assignment3 import Assignment3

class TestAssignment3Bot(unittest.TestCase):

    def test_integrate_poly(self):
        ass3 = Assignment3()
        # Integral of x^2 from 0 to 1 is 1/3
        f = lambda x: x**2
        res = ass3.integrate(f, 0, 1, 100)
        print(f"Integral x^2 [0,1]: {res}")
        self.assertAlmostEqual(res, 1/3, places=5)
        self.assertTrue(isinstance(res, np.float32))

    def test_integrate_sin(self):
        ass3 = Assignment3()
        # Integral of sin(x) from 0 to pi is 2
        f = np.sin
        res = ass3.integrate(f, 0, np.pi, 100)
        print(f"Integral sin(x) [0,pi]: {res}")
        self.assertAlmostEqual(res, 2.0, places=5)

    def test_areabetween_simple(self):
        ass3 = Assignment3()
        # Area between y=x and y=x^2 in [0,1] is 1/6 (~0.166666)
        f1 = lambda x: x
        f2 = lambda x: x**2
        res = ass3.areabetween(f1, f2)
        print(f"Area between x and x^2: {res}")
        # self.assertAlmostEqual(res, 1/6, places=4) # temporarily comment out if needed, or keep. 
        # It failed before because NaN. Let's keep assertion because we expect it to pass now.
        self.assertAlmostEqual(res, 1/6, places=4)

    import math
    def test_areabetween_log_error(self):
        ass3 = Assignment3()
        # Area between ln(x) and 0 in [1, e]. Area = 1.
        # But search range is [-100, 100], so it will hit negative x.
        # Using math.log ensures ValueError is raised.
        f1 = lambda x: math.log(x) if x > 0 else math.nan # simulating math.log behavior usually raises, but let's force it or just use math.log
        
        def f1_strict(x):
            return math.log(x) 
            
        f2 = lambda x: 0
        
        # This should NOT crash with "math domain error"
        res = ass3.areabetween(f1_strict, f2)
        print(f"Area between ln(x) and 0: {res}")
        # Roots are at x=1. Need 2 roots? 
        # ln(x)=0 -> x=1. Only 1 root?
        # If only 1 root, it returns NaN. That is acceptable / correct behavior for areabetween.
        # Key is it shouldn't CRASH.
        pass

if __name__ == '__main__':
    unittest.main()
