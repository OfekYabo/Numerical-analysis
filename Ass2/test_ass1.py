
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
    print("Running Extensive Cache Verification for Assignment 1...")
    
    ass = Assignment1()
    R = RESTRICT_INVOCATIONS
    
    # Define test cases to hit every cache entry
    # (n) -> standard vectorized call
    # (n-1) -> non-vectorized call (triggers fallback)
    
    test_cases = [
        # n = 10 (Cache: 10), Fallback (Cache: 9)
        {'name': 'f2_vec_n10',    'f': f2, 'a': 0, 'b': 5, 'n': 10, 'expect_cache': 10},
        {'name': 'f2_nonvec_n10', 'f': force_non_vectorized(f2), 'a': 0, 'b': 5, 'n': 10, 'expect_cache': 9},
        
        # n = 20 (Cache: 20), Fallback (Cache: 19)
        {'name': 'f4_vec_n20',    'f': f4, 'a': -2, 'b': 4, 'n': 20, 'expect_cache': 20},
        {'name': 'f4_nonvec_n20', 'f': force_non_vectorized(f4), 'a': -2, 'b': 4, 'n': 20, 'expect_cache': 19},
        
        # n = 50 (Cache: 50), Fallback (Cache: 49)
        {'name': 'f3_vec_n50',    'f': f3, 'a': -1, 'b': 5, 'n': 50, 'expect_cache': 50},
        {'name': 'f3_nonvec_n50', 'f': force_non_vectorized(f3), 'a': -1, 'b': 5, 'n': 50, 'expect_cache': 49},
        
        # n = 100 (Cache: 100), Fallback (Cache: 99)
        {'name': 'f13_vec_n100',    'f': f13, 'a': 3, 'b': 10, 'n': 100, 'expect_cache': 100},
        {'name': 'f13_nonvec_n100', 'f': force_non_vectorized(f13), 'a': 3, 'b': 10, 'n': 100, 'expect_cache': 99},
        
        # Constant function optimization check (should return immediately)
        {'name': 'f1_constant_opt', 'f': f1, 'a': 2, 'b': 5, 'n': 20, 'expect_cache': 20},
    ]

    total_time = 0
    passed_count = 0
    
    for i, t in enumerate(test_cases):
        print(f"\nTest {i}: {t['name']}")
        
        # Wrap with restrict invocations to verify budget
        wrapped_f = R(t['n'])(t['f'])
        
        # Verify result/error
        try:
            start_time = time.time()
            res_func = ass.interpolate(wrapped_f, t['a'], t['b'], t['n'])
            duration = time.time() - start_time
            total_time += duration
            
            # Check accuracy
            # We use the original 't['f']' (unwrapped but potentially non-vectorized wrapper) for truth.
            # But the non-vectorized wrapper works fine for single point evaluation loop.
            base_func = t['f']
            
            check_n = 2 * t['n']
            xs = np.random.uniform(t['a'], t['b'], check_n)
            
            # For truth, simply call original f2/f4 etc. to avoid wrapper overhead/issues
            orig_func_map = {f2: f2, f4: f4, f3: f3, f13: f13, f1: f1}
            # Extract original function if wrapped
            true_func = None
            if hasattr(base_func, '__name__') and 'nonvec' in base_func.__name__:
                 # Find the original function by behavior or just mapping manually for this script
                 if 'f2' in t['name']: true_func = f2
                 elif 'f4' in t['name']: true_func = f4
                 elif 'f3' in t['name']: true_func = f3
                 elif 'f13' in t['name']: true_func = f13
            else:
                true_func = base_func

            avg_err = 0
            for x in xs:
                # result of interpolate
                y_res = res_func(x)
                # result of truth
                y_true = true_func(x)
                avg_err += abs(y_res - y_true)
            
            avg_err /= check_n
            
            print(f"  Time: {duration:.5f}s")
            print(f"  Mean Error: {avg_err:.5e}")
            
            if avg_err < 1e-3:
                print("  Status: PASSED")
                passed_count += 1
            else:
                print("  Status: HIGH ERROR (Check if expected)")
                
        except EOFError:
            print("  Status: FAILED (Exceeded Invocations)")
        except Exception as e:
            print(f"  Status: FAILED ({e})")
            import traceback
            traceback.print_exc()

    print(f"\nTotal Passed: {passed_count}/{len(test_cases)}")

if __name__ == "__main__":
    run_grader_simulation()
