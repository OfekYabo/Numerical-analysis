
import numpy as np
import time
from assignment1 import Assignment1
from functionUtils import RESTRICT_INVOCATIONS

np.random.seed(42)  # Fixed seed

def run_log_killer():
    print("Running Log Heuristic Safety Check (The Killer Test)...")
    
    ass = Assignment1()
    R = RESTRICT_INVOCATIONS
    
    # KILLER FUNCTION: Shifted Parabola
    # f(x) = x^2 + epsilon
    # Domain: [-1, 1]
    # Min: epsilon, Max: 1 + epsilon
    # Ratio: approx 1/epsilon (HUGE) -> Triggers Heuristic
    # Log Domain: ln(x^2 + e). Near x=0, this is a deep "well". 
    # Polynomial interpolation should struggle mightily.
    
    epsilon = 1e-6
    def f_killer(x):
        return x**2 + epsilon

    a, b, n = -1, 1, 20
    
    print(f"Function: x^2 + {epsilon}")
    print(f"Range: [{a}, {b}]")
    print(f"n: {n}")
    
    wrapped_f = R(n)(f_killer)
    
    try:
        res_func = ass.interpolate(wrapped_f, a, b, n)
        
        # Verify
        check_n = 200
        xs = np.linspace(a, b, check_n)
        avg_err = 0
        max_err = 0
        
        for x in xs:
            y_res = res_func(x)
            y_true = f_killer(x)
            err = abs(y_res - y_true)
            avg_err += err
            max_err = max(max_err, err)
        
        avg_err /= check_n
        
        print(f"Mean Error: {avg_err:.5e}")
        print(f"Max Error:  {max_err:.5e}")
        
        if avg_err > 1e-2:
            print("Status: FAILED (SAFETY HAZARD DETECTED)")
            print("Reason: Heuristic triggered on polynomial, caused massive error.")
        else:
            print("Status: PASSED (Safe)")
            
    except Exception as e:
        print(f"Status: CRASHED ({e})")

if __name__ == "__main__":
    run_log_killer()
