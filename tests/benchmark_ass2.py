
import sys
import os
import time
import importlib.util
import numpy as np
import pandas as pd

# Path setup to access Ass4/Ass3 modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Ass4')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Ass3')))

# Import boilerplate from commons/grader logic if needed, but we'll recreate the test logic 
# to ensure it's exactly what we want (clean usage of Ass2).
from commons import f1, f2, f2_nr, f3_nr, f10, f12, f13
from functionUtils import SAVEARGS

# Mock report System
class MockGrader:
    def __init__(self):
        self.reports = []
    
    def grade_assignment(self, function, params, assignment_name, func_error, expected_results, repeats):
        # measure time and error
        start = time.time()
        
        errors = []
        
        for i, (param, expected, check_err) in enumerate(zip(params, expected_results, func_error)):
             # Run 'repeats' times
             for _ in range(repeats):
                 res = function(**param)
            
             # Check error on last run
             try:
                 err = check_err(res, expected)
                 errors.append(err)
             except Exception as e:
                 errors.append(f"Error: {e}")
                 
        total_time = (time.time() - start) / (repeats * len(params)) # Avg time per call
        
        return errors, total_time

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_roots(f1, f2, res, gt, maxerr):
    err = 0

    # Safety for None
    if res is None: return 100
    
    # count non roots
    # res = [x for x in res] # Already likely list/iterable
    # print(res)

    for x in res:
        if (abs(f1(x) - f2(x)) > maxerr):
            err += 1
            # print("ERR:", x, f1(x), f2(x), abs(f1(x) - f2(x)))

    # count missing roots
    gt = [x for x in gt]

    res = np.array(list(res)) # Force list then array
    if len(res) == 0:
        return len(gt) # All missing

    for gtr in gt:
        # find the closest entry in res:
        dist = abs(res - gtr)
        i = np.argmin(dist)
        x = float(res[i])
        found_close = False
        
        # Original grader logic: scan linspace between found and expected
        for y in np.linspace(min(x, gtr), max(x, gtr), 10):
            if abs(f1(y) - f2(y)) > maxerr:
                # If function deviates too much in the gap, it implies they are different roots 
                # or not close enough on the manifold.
                # However, for pure root matching, this logic is specific.
                # Let's keep it exactly as is to match grader.
                err += 1
                # print("MISS:", gtr, x, abs(f1(x) - f2(x)))
                found_close = False
                break
            else:
                found_close = True
                
        # If the loop finished without break? 
        # Wait, the grader adds err if break happens.
        # It DOES NOT explicitly count 'found'. It assumes found unless proven otherwise by the linspace check?
        # NO. The loop checks if the path between found 'x' and real 'gtr' is valid (close to 0).
        # If valid, it DOES NOT increment err.
        
    return err

def run_benchmark(assignment_class, name, repeats):
    ass2 = assignment_class()
    grader = MockGrader()
    
    # --- Assignment 2 Tests (Intersections) ---
    names = ('f1',   'f2',  'a',    'b')
    valss = [(f2_nr, f3_nr, 0.5,    2),
             (f3_nr, f10,   1,      10),
             (f1,    f2_nr, -2,     5),
             (f12,   f13,   -0.5,   1.5)]
             
    params = [dict(zip(names, vals)) for vals in valss]
    
    expected_results = [
        [0.671718, 1.8147],
        [1.62899, 2.69730, 2.89186388, 3.725809, 3.7914655],
        [-0.79128, 3.79128],
        [-0.175390, 1.42539]
    ]

    # Error Function Wrapper
    func_error = []
    for f1_f, f2_f, a_f, b_f in valss:
        def make_checker(f1_c, f2_c):
            return lambda res, exp: test_roots(f1_c, f2_c, res, exp, 0.001)
        func_error.append(make_checker(f1_f, f2_f))

    ass2_errors, ass2_time = grader.grade_assignment(
        ass2.intersections, params, 'Ass2', func_error, expected_results, repeats
    )
    
    # --- Assignment 3 Tests (Area) ---
    # This checks impact on Areabetween (which depends on Ass2)
    # Note: We need Assignment3 instance that uses THIS Ass2.
    # Since Assignment3 dynamically imports, we can hack it by patching sys.modules or just trusting it picks up assignment2.py
    # But here we are just testing 'assignment2' performance implicitly if we ran Ass3.
    # Actually, let's just create a synthetic Area test that uses 'intersections' directly to isolate Ass2 perf.
    
    return {
        "Name": name,
        "Ass2 Mean Time": ass2_time,
        "Ass2 Total Error": sum([e if isinstance(e, (int, float)) else 100 for e in ass2_errors]),
        "Errors": ass2_errors
    }

def main():
    REPEATS = 20 # Higher repeats for precision
    
    print(f"Running Benchmark (Repeats={REPEATS})...")
    
    # Load OLD
    mod_old = load_module("assignment2_old", "Ass4/assignment2_old.py")
    res_old = run_benchmark(mod_old.Assignment2, "OLD (9.7)", REPEATS)
    
    # Load NEW
    mod_new = load_module("assignment2_new", "Ass4/assignment2_new.py")
    res_new = run_benchmark(mod_new.Assignment2, "NEW (Robust)", REPEATS)
    
    # Compare
    df = pd.DataFrame([res_old, res_new])
    print("\n=== BENCHMARK RESULTS ===")
    print(df[["Name", "Ass2 Mean Time", "Ass2 Total Error"]])
    print("\nDetailed Errors:")
    print(f"OLD: {res_old['Errors']}")
    print(f"NEW: {res_new['Errors']}")
    
    ratio = res_old['Ass2 Mean Time'] / res_new['Ass2 Mean Time']
    print(f"\nSpeedup Factor (Old/New): {ratio:.2f}x")
    if ratio > 1:
        print("(New is faster)")
    else:
        print("(Old is faster)")

if __name__ == "__main__":
    main()
