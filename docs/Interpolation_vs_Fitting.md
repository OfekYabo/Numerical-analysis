# Interpolation (Ass1) vs. Curve Fitting (Ass4)

## 1. The Core Difference

| Feature | **Interpolation (Ass1)** | **Curve Fitting / Approximation (Ass4)** |
| :--- | :--- | :--- |
| **Goal** | Pass **exactly** through every data point. | Find a smooth curve that gets **close** to the points (minimize error). |
| **Input Data** | Assumed to be "Clean" (Precise). | Assumed to be **Noisy** (Errors in measurement). |
| **Result** | A polynomial of degree $N-1$ for $N$ points. | A polynomial of degree $d$ (where $d \ll N$). |
| **Risk** | **Runge's Phenomenon**: If you force a curve through noisy points, it oscillates wildly. | **Underfitting**: If degree $d$ is too low, it won't capture the shape. |

### Visual Analogy
*   **Interpolation**: Connecting the dots in a kid's drawing book. You strictly go from dot 1 to dot 2 to dot 3. If one dot is off, the line jerks.
*   **Fitting**: Drawing a smooth "trend line" through a scatter plot. You ignore individual outliers to capture the general direction.

## 2. Why Different Methods?

### Assignment 1 (Interpolation)
*   **Method Used**: **Barycentric Lagrange Interpolation** (with Chebyshev Nodes).
*   **Why?**: We didn't need to solve a system of equations ($A x = b$). There is a direct **closed-form formula** to construct the polynomial if we choose smart points (Chebyshev).
*   **Complexity**: $O(N)$ to evaluate. No matrix inversion needed.

### Assignment 4 (Curve Fitting)
*   **Method Used**: **Least Squares (Normal Equations)**.
*   **Why?**: There is no single curve that passes through all points. We had to find the "best" coefficients $c$ that minimize the error squared. This mathematically requires solving a derivative equals zero, which leads to a system of linear equations:
    $$(A^T A) c = A^T y$$
*   **New Math**: This is why we implemented **Gaussian Elimination** and **Matrix Multiplication** for the first time in this project. We never needed to solve a linear system in Ass1 or Ass2.

## Summary of Tech Stack
*   **Ass2 (Roots)**: Iterative methods (Newton/Bisection). No Linear Algebra.
*   **Ass1 (Interpolation)**: Direct Formula (Barycentric). No Linear Algebra.
*   **Ass4 (Fitting)**: Linear Algebra (Matrices, Gaussian Elimination). **First time use**.
