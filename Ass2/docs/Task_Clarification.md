# Task Clarification: Interpolation (Assignment 1)

## Overview
The goal is to implement an interpolation method that takes a function `f`, a range `[a, b]`, and a maximum number of sample points `n`. The method returns a callable object (function) `g` that approximates `f` within the given range.

## Input specifications
- **Function**: `f` (callable).
- **Range**: `[a, b]` (floats).
- **Points budget**: `n` (int).
- **Constraints**:
  - `n <= 100`.
  - You must not call `f` more than `n` times.
  - Calling more than `n` times raises an exception and fails the test.

## Output specifications
- **Return**: A callable function `g(x)`.
- **Behavior**: `g(x)` will be called with various `x` values in `test_with_poly` and other tests to measure error.

## Grading Criteria
1.  **Accuracy**: Minimizing the average absolute error `|f(x) - g(x)|` at random points.
2.  **Performance (Runtime)**:
    - O(n) solutions are preferred and graded higher (5-10 pts).
    - O(n^2) solutions are graded lower (0-8 pts).
    - "O(n)" likely refers to the complexity of the interpolation setup or the per-point evaluation logic, considering the context of "high performance". Efficient evaluation is key.
3.  **Test Cases**:
    - `n` values: 1, 10, 20, 50, 100.
    - Functions: Varying, but **at least half are polynomials**.
    - Polynomials will have degrees up to high orders.
    - Other functions include trigonometric, exponential, log, and combinations.

## Limitations & Rules
- **Language**: Python 3.
- **Allowed Libraries**: Standard libraries, limited `numpy`, `pytorch`.
- **Forbidden Methods**:
  - Built-in interpolation functions (e.g., `numpy.interp`, `scipy.interpolate`, `polyfit`).
  - Using these results in heavy penalties (up to 60%).
- **Forbidden Actions**:
  - `f` calls > `n`.
  - Collaboration/Plagiarism.

## Strategy Implication
- Since many test cases are polynomials, a method that is exact or highly accurate for polynomials (like polynomial interpolation) is advantageous.
- **Chebyshev Nodes**: Using Chebyshev nodes avoids Runge's phenomenon and minimizes max error for polynomial interpolation. This is superior to equidistant points.
- **Barycentric Interpolation**: Allows O(n) evaluation (or faster) and is numerically stable.
- **Splines**: Linear splines are guaranteed 5 points but likely won't win the "contest" for high accuracy on polynomials compared to global polynomial interpolation on Chebyshev nodes.
