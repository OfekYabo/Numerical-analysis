# Numerical Analysis Project Overview

This project consists of 5 assignments focusing on numerical methods, accuracy, and performance (runtime). 

## Project Structure and Task Order
The folders are named `Ass1` to `Ass5`, but the logical order of tasks (by release/dependency) is:
1. **Assignment 2** (Found in `Ass1` folder): Root Finding.
2. **Assignment 1** (Found in `Ass2` folder): Interpolation.
3. **Assignment 4** (Found in `Ass3` folder): Curve Fitting / Least Squares.
4. **Assignment 3** (Found in `Ass4` folder): Integration and Area Between Curves.
5. **Assignment 5** (Found in `Ass5` folder): 2D Shape Fitting and Area Calculation.

## Grading Criteria
- **Correctness & Accuracy**: Primary grade component. Methods must meet specified error bounds (`maxerr`).
- **Performance (Timing)**: Secondary grade component. Algorithms are constrained by running time (e.g., `maxtime` argument). 
    - *Note*: Even where timing isn't explicitly mentioned, efficient code is critical (O(n) vs O(n^2)).
- **Precision**: Use `float32` where specified (e.g., Assignment 3) to manage floating-point errors.

## Assignments Breakdown

### 1. Root Finding (Assignment 2)
- **Goal**: Find intersection points of two functions `f1` and `f2` in a range `[a, b]`.
- **Key Challenges**: Handling multiple roots, closely spaced roots, and ensuring high precision using Hybrid Newton-Bisection.

### 2. Interpolation (Assignment 1)
- **Goal**: Interpolate a function `f` using at most `n` points.
- **Key Challenges**: Minimizing error and runtime.
- **Techniques**: Chebyshev nodes, Barycentric interpolation, Adaptive methods (e.g., Log-Interpolation for exponential functions).

### 3. Curve Fitting (Assignment 4)
- **Goal**: Fit a model function (polynomial of degree `d`) to noisy sampled data.
- **Key Challenges**: Minimizing Mean Squared Error (MSE) under time constraints. Handling noise and delays.
- **Constraints**: No external optimization libraries allowed.

### 4. Integration (Assignment 3)
- **Goal**: Calculate definite integrals and area enclosed between two functions.
- **Key Challenges**: 
    - Calculating area requires finding intersection points (Dependency on Ass2).
    - Integrating "hard" functions (oscillating, etc.).
    - Use `float32` precision.

### 5. Shape Fitting & Area (Assignment 5)
- **Goal**: Fit a model to a 2D closed shape contour given noisy samples and calculate its area.
- **Key Challenges**: 
    - Optimization loop must respect `maxtime` (strict 5s limit).
    - Minimizing least squares error for the shape model.
    - Calculating area of the fitted model.
