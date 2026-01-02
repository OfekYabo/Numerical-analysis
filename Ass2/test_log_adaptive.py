
import numpy as np
import time
from commons import *
from assignment1 import Assignment1
from functionUtils import RESTRICT_INVOCATIONS

np.random.seed(42)

def force_non_vectorized(f):
    """Wraps a function to ensure it raises an error if called with an array."""
    def wrapper(x):
        if isinstance(x, np.ndarray) and x.ndim > 0 and x.size > 1:
            raise ValueError("Vectorization forced failure for testing fallback")
        return f(x)
    wrapper.__name__ = f.__name__ + "_nonvec"
    return wrapper

def run_grader_simulation():
    print("Running Experimental Adaptive Log Check...")
    
    ass = Assignment1()
    R = RESTRICT_INVOCATIONS
    
    # We focus on f8 (should improve massive) and f4 (should be perfect)
    # And check regressions on others like f2 (polynomial) which shouldn't trigger log
    
    test_cases = [
        # Check Improvement: f8 (Double Exp)
        {'name': 'f8_adaptive', 'f': f8, 'a': 1, 'b': 3, 'n': 10},
        
        # Check Improvement: f4 (Gaussian) - huge dynamic range > 1000
        {'name': 'f4_adaptive', 'f': f4, 'a': -2, 'b': 4, 'n': 20},
        
        # Check Regression: f2 (Poly) - negative values, should NOT trigger log
        {'name': 'f2_regression', 'f': f2, 'a': 0, 'b': 5, 'n': 10},
        
        # Check Regression: f3 (Poly+Sin) - min is near -1, should NOT trigger log
        {'name': 'f3_regression', 'f': f3, 'a': -1, 'b': 5, 'n': 50},
    ]

    total_time = 0
    passed_count = 0
    
    for i, t in enumerate(test_cases):
        print(f"\nTest {i}: {t['name']}")
        
        wrapped_f = R(t['n'])(t['f'])
        
        try:
            start_time = time.time()
            res_func = ass.interpolate(wrapped_f, t['a'], t['b'], t['n'])
            duration = time.time() - start_time
            total_time += duration
            
            base_func = t['f']
            check_n = 2 * t['n']
            xs = np.random.uniform(t['a'], t['b'], check_n)
            
            avg_err = 0
            for x in xs:
                y_res = res_func(x)
                y_true = base_func(x)
                avg_err += abs(y_res - y_true)
            
            avg_err /= check_n
            
            print(f"  Time: {duration:.5f}s")
            print(f"  Mean Error: {avg_err:.5e}")
            
            # Acceptance criteria
            if 'f8' in t['name']:
                # Previous error was ~6e6. We expect HUGE improvement.
                if avg_err < 100: 
                     print("  Status: IMPROVED (Massively)")
                else:
                     print("  Status: WEAK IMPROVEMENT")
            elif 'f4' in t['name']:
                # Previous error ~1e-3. Should be near machine epsilon now.
                if avg_err < 1e-10:
                     print("  Status: PERFECT (Log Trick Worked)")
                else:
                     print("  Status: NORMAL (Log Trick Failed/Skipped)")
            else:
                # Regressions
                if avg_err < 1e-10:
                    print("  Status: PASSED (No Regression)")
                else:
                    print("  Status: CHECK (Regression?)")

        except Exception as e:
            print(f"  Status: FAILED ({e})")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    run_grader_simulation()
