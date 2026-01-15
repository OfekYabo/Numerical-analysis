import sys
import os
import time
import numpy as np
import pandas as pd
import importlib.util

# Ensure we can import Assignment4
# It is located in Ass3/assignment4.py
sys.path.append(os.path.join(os.getcwd(), 'Ass3'))

try:
    from assignment4 import Assignment4
except ImportError:
    # Fallback if running directly inside Ass3 or if file is moved
    try:
        from Ass3.assignment4 import Assignment4
    except ImportError:
        print("CRITICAL ERROR: Could not import 'Assignment4'. Make sure 'Ass3/assignment4.py' exists.")
        sys.exit(1)

def generate_test_data(poly_coeffs, a, b, num_points=100, noise_std=0.1):
    """Generates noisy data from a polynomial."""
    x = np.linspace(a, b, num_points)
    y_true = np.polyval(poly_coeffs, x)
    noise = np.random.normal(0, noise_std, num_points)
    y_noisy = y_true + noise
    
    # Create the function f(x) that returns individual points (simulating function call)
    # In reality, fit receives a callable f(x) -> y
    # Note: Assignment 4 fit signature is fit(f, a, b, d, maxtime)
    # We need to wrap our data as a function
    def f(arr_x):
        # Handle scalar or array input
        if np.isscalar(arr_x):
            return np.polyval(poly_coeffs, arr_x) + np.random.normal(0, noise_std)
        return np.polyval(poly_coeffs, arr_x) + np.random.normal(0, noise_std, len(arr_x))
    
    return f, y_true

def run_test(degree, maxtime=5.0):
    """Runs a single test case."""
    
    # 1. Setup Test Case
    ass4 = Assignment4()
    
    # Random polynomial coefficients
    coeffs = np.random.uniform(-5, 5, degree + 1)
    a, b = -2, 2
    
    f, _ = generate_test_data(coeffs, a, b, num_points=200, noise_std=0.05)
    
    # 2. Run fit()
    start_time = time.time()
    try:
        fitted_f = ass4.fit(f, a, b, degree, maxtime)
        end_time = time.time()
        elapsed_time = end_time - start_time
    except Exception as e:
        return {
            "Test Name": f"Poly Degree {degree}",
            "Degree": degree,
            "MSE": "N/A",
            "Time": "N/A",
            "Status": "FAIL",
            "Message": f"Exception: {str(e)}"
        }

    # 3. Validation
    # Generate new points to test the fitted function against the true underlying process (without noise for truth)
    # Note: fitted_f returns a function
    x_val = np.linspace(a, b, 100)
    y_true_val = np.polyval(coeffs, x_val)
    
    try:
        y_pred = np.array([fitted_f(xi) for xi in x_val])
        mse = np.mean((y_true_val - y_pred) ** 2)
    except Exception as e:
         return {
            "Test Name": f"Poly Degree {degree}",
            "Degree": degree,
            "MSE": "N/A",
            "Time": elapsed_time,
            "Status": "FAIL",
            "Message": f"Prediction Error: {str(e)}"
        }
    
    status = "PASS"
    msg = "OK"
    
    if elapsed_time > maxtime:
        status = "FAIL"
        msg = f"Time Limit Exceeded ({elapsed_time:.4f} > {maxtime})"
    elif mse > 0.1: # Threshold depends on noise, 0.1 is generous for 0.05 noise
        status = "FAIL"
        msg = f"High MSE ({mse:.6f})"
        
    return {
        "Test Name": f"Poly Degree {degree}",
        "Degree": degree,
        "MSE": mse,
        "Time": elapsed_time,
        "Status": status,
        "Message": msg
    }

def main():
    print("Running Grading Tests...")
    results = []
    
    # 1. Polynomial Tests (Degrees 1-15)
    for d in range(1, 16):
        print(f"Testing Degree {d}...", end="\r")
        res = run_test(degree=d, maxtime=5)
        results.append(res)

    # 2. Non-Polynomial Tests
    print("\nRunning Non-Polynomial Tests...")
    
    # Test SINE function
    # fit(sin(x), 0, 2pi, d=10) -> Should fit well (Taylor series)
    print("Testing Sin(x)...", end="\r")
    f_sin = lambda x: np.sin(x)
    res_sin = run_test_custom(f_sin, "Sin(x)", 0, 2*np.pi, degree=10)
    results.append(res_sin)

    # Test EXP function
    # fit(e^x, 0, 2, d=5)
    print("Testing Exp(x)...", end="\r")
    f_exp = lambda x: np.exp(x)
    res_exp = run_test_custom(f_exp, "Exp(x)", 0, 2, degree=5)
    results.append(res_exp)
    
    # Test 1/log(x) (Function f7 from grader)
    # fit(1/log(x), 3, 16, d=10)
    print("Testing 1/log(x)...", end="\r")
    f_log = lambda x: 1.0/np.log(x) # Range [3, 16] is safe from x=1
    res_log = run_test_custom(f_log, "1/log(x)", 3, 16, degree=10)
    results.append(res_log)

    # Test Double Exponential f8 (e^e^x)
    # fit(e^e^x, 0, 1, d=15)
    print("Testing e^(e^x) (f8)...", end="\r")
    f_f8 = lambda x: np.exp(np.exp(x))
    res_f8 = run_test_custom(f_f8, "Exp(Exp(x))", 0, 1, degree=15)
    results.append(res_f8)

    print("\nTests Completed.")
    
    # Create DataFrame and Save
    df = pd.DataFrame(results)
    
    # Reorder columns
    df = df[["Test Name", "Degree", "MSE", "Time", "Status", "Message"]]
    
    print("\n=== Summary ===")
    print(df)
    
    output_file = "results.csv"
    df.to_csv(output_file, index=False)
    print(f"\nResults saved to '{output_file}'.")

def run_test_custom(target_func, name, a, b, degree, maxtime=5.0, noise_std=0.05):
    """Runs a specific test case for a given function."""
    ass4 = Assignment4()
    
    # Wrap target function with noise
    def f_noisy(arr_x):
        if np.isscalar(arr_x):
            return target_func(arr_x) + np.random.normal(0, noise_std)
        return target_func(arr_x) + np.random.normal(0, noise_std, len(arr_x))

    # Run fit
    start_time = time.time()
    try:
        fitted_f = ass4.fit(f_noisy, a, b, degree, maxtime)
        elapsed_time = time.time() - start_time
    except Exception as e:
        return {"Test Name": name, "Degree": degree, "MSE": "N/A", "Time": "N/A", "Status": "FAIL", "Message": str(e)}

    # Validation
    x_val = np.linspace(a, b, 200)
    y_true = target_func(x_val)
    
    try:
        y_pred = np.array([fitted_f(xi) for xi in x_val])
        mse = np.mean((y_true - y_pred) ** 2)
    except Exception as e:
         return {"Test Name": name, "Degree": degree, "MSE": "N/A", "Time": elapsed_time, "Status": "FAIL", "Message": f"Pred Error: {str(e)}"}
    
    status = "PASS"
    msg = "OK"
    if elapsed_time > maxtime + 0.1: status = "FAIL"; msg = f"Timeout ({elapsed_time:.3f})"
    elif mse > 0.1: status = "FAIL"; msg = f"High MSE ({mse:.5f})"

    return {"Test Name": name, "Degree": degree, "MSE": mse, "Time": elapsed_time, "Status": status, "Message": msg}

if __name__ == "__main__":
    main()
