# Current Implementation Summary

This document summarizes the algorithms and logic implemented for the completed assignments (1 and 2).

## Assignment 2 (Root Finding)
**Location**: `Ass1/assignment2.py`
**Status**: Implemented

### Logic
The `intersections` method finds roots for $f(x) = f_1(x) - f_2(x) = 0$.
1. **Scanning**: The interval $[a, b]$ is scanned with a step size `(b-a)/N_STEPS` to detect sign changes.
   - *Optimization*: Uses a dynamic step size to avoid missing roots, though fixed scanning is the primary driver.
2. **Hybrid Newton-Bisection**:
   - When a bracket $[x_{prev}, x_{curr}]$ containing a root is found (sign change), `_find_root` is called.
   - Tries **Newton-Raphson** steps first.
   - Falls back to **Bisection** if:
     - Derivative is too small (ZeroDivision).
     - Newton step jumps out of the bracket.
3. **Filtering**: Sorts roots and removes duplicates based on `maxerr` to ensure unique intersection return values.

## Assignment 1 (Interpolation)
**Location**: `Ass2/assignment1.py`
**Status**: Implemented

### Logic
The `interpolate` method approximates a function $f(x)$ using $n$ Chebyshev nodes.
1. **Chebyshev Nodes**: Uses extrema of Chebyshev polynomials of the second kind (mapped to $[a, b]$) to minimize Runge's phenomenon.
2. **Barycentric Interpolation**:
   - Pre-calculates weights $w_j$ for the nodes (Checking a cache for performance).
   - Evaluates the polynomial using the Barycentric formula (Second form) for numerical stability (O(n) evaluation).
3. **Optimizations**:
   - **Vectorization Check**: Attempts to call $f$ on the entire vector of nodes once. If successful, saves $n-1$ calls.
   - **Constant Function Detection**: Returns a constant lambda if vectorization returns a scalar.
   - **Adaptive Log-Interpolation**: Detects if the function spans a huge dynamic range (e.g., $e^x$) and strictly positive. If so, interpolates $\ln(f(x))$ instead of $f(x)$ for massive accuracy gains on exponential functions.
