import sys
import os
import time
import numpy as np
from numpy.random import uniform
import unittest

sys.path.append(os.getcwd())

import assignment1
from functionUtils import RESTRICT_INVOCATIONS, SAVEARGS
from commons import * 

def run_test():
    try:
        gr = assignment1.Assignment1()
        
        # Test cases from grader.py
        R = RESTRICT_INVOCATIONS
        
        # Mapping definition from grader logic
        valss=[(R(10)(f2) ,0  ,5  ,10 ),
               (R(20)(f4) ,-2 ,4  ,20 ),
               (R(50)(f3) ,-1 ,5  ,50 ),
               (R(20)(f13),3  ,10 ,20 ),
               (R(20)(f1) ,2  ,5  ,20 ),
               (R(10)(f7) ,3  ,16 ,10 ),
               (R(10)(f8) ,1  ,3  ,10 ),
               (R(10)(f9) ,5  ,10 ,10 ),]
        
        # List of original functions corresponding to valss
        orig_funcs = [f2, f4, f3, f13, f1, f7, f8, f9]
        
        print("Running Grader-like Tests for Assignment 1...")
        
        total_mean_err = 0
        
        for i, (f_restricted, a, b, n) in enumerate(valss):
            f_orig = orig_funcs[i]
            
            print(f"Test {i}: f={f_orig.__name__}, a={a}, b={b}, n={n}")
            
            params = {'f': f_restricted, 'a': a, 'b': b, 'n': n}
            
            start_t = time.time()
            try:
                res_func = gr.interpolate(**params)
            except Exception as e:
                print(f"  FAILED with exception: {e}")
                continue
                
            end_t = time.time()
            
            # Validation: Mean abs error at 2*n points
            err_sum = 0
            count = 2 * n
            test_points = uniform(low=a, high=b, size=count)
            
            for x in test_points:
                try:
                    val_res = res_func(x)
                    val_orig = f_orig(x)
                    err_sum += abs(val_res - val_orig)
                except Exception as e:
                    print(f"  Error evaluating result at x={x}: {e}")
            
            mean_err = err_sum / count
            total_mean_err += mean_err
            
            print(f"  Time: {end_t - start_t:.5f}s")
            print(f"  Mean Err: {mean_err:.5e}")
            
            if mean_err > 1e-3:
                 print("  WARNING: Error > 1e-3")
            else:
                 print("  PASSED (Low Error)")
                 
        print(f"Average Mean Error across tests: {total_mean_err / len(valss):.5e}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
