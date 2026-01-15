# Assignment 4 Implementation Plan: Curve Fitting

## Goal
Fit a function (polynomial) to noisy data sampled from a "clean" function.
- **Input**: `f` (noisy function), `a`, `b` (range), `d` (degree), `maxtime`.
- **Output**: A python function (polynomial) that minimizes MSE against the noisy data (which approximates the clean function).

## Constraints & Penalties
The project documentation specifies severe penalties for standard fitting tools:
- `numpy.polyfit`: **40% penalty**.
- `lstsq` (Least Squares): **60% penalty** in Ass4.
- `numpy.linalg.solve`: **15% penalty**.
- **Requirement**: "You should not use those parts of the libraries that implement numerical methods taught in this course." -> This strongly implies we must implement our own **Linear System Solver**.

## Strategy: Manual Least Squares

To find the polynomial coefficients $c = [c_0, c_1, ..., c_d]$ for $P(x) = c_0 + c_1 x + ... + c_d x^d$, we solve the **Normal Equations**:
$$ (A^T A) c = A^T y $$

Where $A$ is the Vandermonde matrix of sampled points.

### Steps
1.  **Sampling**:
    - Sample $N$ points from $f(x)$ in $[a, b]$.
    - $N$ should be large enough to average out noise (e.g., $N > 10d$ or dynamic based on time).
    - Since we have a strict time limit (`maxtime`), we must balance $N$.
    
2.  **Matrix Construction**:
    - Build $A^T A$ (Matrix of size $(d+1) \times (d+1)$).
    - Build $A^T y$ (Vector of size $d+1$).
    - *Optimization*: We can compute these sums directly without storing the huge $N \times (d+1)$ matrix $A$.
        - $(A^T A)_{ij} = \sum x_k^{i+j}$
        - $(A^T y)_i = \sum y_k x_k^i$
        - This is $O(N \cdot d)$ instead of matrix multiplication.

3.  **Solving Linear System (Custom Implementation)**:
    - Since `numpy.linalg.solve` is penalized, we strictly implement **Gaussian Elimination** or **LU Decomposition**.
    - Given the system $M c = v$ (where $M = A^T A, v = A^T y$), solve for $c$.
    - Size of $M$ is small ($(d+1) \times (d+1)$). Even for $d=20$, this is instant.

4.  **Handling Non-Polynomials (5% of cases)**:
    - The instructions say "5% will be non-polynomials".
    - Usually, `fit` is asked to return a polynomial of degree `d` even if the source isn't one (best fit).
    - Taylor expansion ensures it's a good approximation locally.

## Detailed Algorithm

### 1. `fit(f, a, b, d, maxtime)`
- Start timer.
- Determine sampling budget $N$.
    - Safe default: $N = 1000$ to $5000$.
- Generate $x$ points: `np.linspace(a, b, N)`.
- Generate $y$ points: `f(x)`.
- Construct Matrix $M$ ($d+1 \times d+1$) and Vector $v$ ($d+1$).
    - Powers of $x$: Precompute $x^0, x^1, \dots, x^{2d}$.
    - Fill $M_{ij} = \text{sum}(x^{i+j})$.
    - Fill $v_i = \text{sum}(y \cdot x^i)$.
- **Solve $M c = v$ using `custom_solve(M, v)`**.
- Return `lambda x: poly_val(c, x)`.

### 2. `custom_solve(A, b)`
- Input: Matrix $A$ ($n \times n$), Vector $b$ ($n$).
- Algorithm: **Gaussian Elimination with Partial Pivoting**.
    - Forward Elimination:
        - For each column $k$:
            - Find pivot (max abs value in column $k$ below diagonal). Swap rows.
            - Eliminate entries below pivot.
    - Backward Substitution:
        - Solve for $x$.

### 3. `poly_val(c, x)`
- Horner's Method for stability and speed.
- $P(x) = c_0 + x(c_1 + x(c_2 + \dots))$
