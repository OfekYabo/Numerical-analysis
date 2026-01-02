# Methods and Design: High-Performance Interpolation

## 1. Problem Analysis
The task requires interpolating a function $f$ on $[a, b]$ using at most $n$ points. We aim to minimize average absolute error.
Key factors:
- **Test Set**: "At least half ... are polynomials".
- **Constraint**: Strict limit on function calls ($n$).
- **Performance**: High value placed on $O(n)$ complexity and accuracy.

## 2. Methodology Selection

### Option A: Piecewise Linear / Cubic Splines
- **Pros**: Robust, local.
- **Cons**: Error decays as $O(1/n^2)$ or $O(1/n^4)$. For high-degree polynomials (which are smooth), this is essentially "losing info" compared to a global method that could capture the polynomial exactly.
- **Verdict**: Good fallback, but likely not the "winning" high-performance solution for polynomial-heavy test sets.

### Option B: Equidistant Polynomial Interpolation
- **Pros**: Simple Concept.
- **Cons**: **Runge's Phenomenon**. As $n$ increases, error oscillation near boundaries explodes for some functions ($1/(1+25x^2)$).
- **Verdict**: Unsuitable for general robust interpolation with large $n$.

### Option C: Cubic Splines (via Thomas Algorithm)
- **Concept**: Connect points with piecewise cubic polynomials, ensuring continuity of $f, f', f''$.
- **Implementation**: Requires solving a tridiagonal linear system for the second derivatives at knots. This is done efficiently using the **Thomas Algorithm** (TDMA).
- **Complexity**: $O(n)$ to solve the system (Thomas Algo) and $O(1)$ to evaluate (if grid is uniform, otherwise $O(\log n)$ to find interval).
- **Pros**: 
  - $O(n)$ performance (excellent).
  - Very smooth, no Runge's phenomenon.
  - Good for functions with local erratic behavior.
- **Cons**: 
  - **Accuracy limit**: Error decays as $O(1/n^4)$. For analytic functions (like polynomials), this is **much worse** than the spectral accuracy ($O(e^{-cn})$) of Chebyshev interpolation.
  - Since the task prioritizes "minimizing error" and mentions many test cases are polynomials, Splines will strictly lose to Global Polynomial Interpolation on those cases.
- **Verdict**: Strong contender, but inferior to Chebyshev for this specific contest.

### Option D: Chebyshev Polynomial Interpolation (Barycentric Form)
- **Concept**: Sample $f$ at **Chebyshev nodes** (roots or extrema of Chebyshev polynomials).
- **Pros**:
  - **Minimizes Runge's Phenomenon**: The interpolation is numerically stable and converges for any Lipschitz continuous function.
  - **Exact for Polynomials**: If $f$ is a polynomial of degree $< n$, this method reconstructs it **exactly** (within machine epsilon).
  - **Efficiency**: The **Barycentric Interpolation Formula** allows evaluation in $O(n)$ time. Calculating weights is $O(n)$ (or $O(1)$ known analytically).
- **Verdict**: **The Best Approach**. It maximizes the score on the polynomial subset (exact match) and provides the optimal polynomial approximation for general continuous functions.

## 3. Simplified Explanation: What are we actually doing?

### The "Rug" Analogy (Why not equal points?)
Imagine you are trying to nail a rug flat against a floor.
-   **Equidistant Points**: If you put nails at equal distances (like 1cm apart), the edges of the rug tend to flap wildly and curl up. This is **Runge's Phenomenon**. It happens because polynomials wiggle a lot at the edges if you don't pin them down there.
-   **Chebyshev Points**: These points are clustered tightly at the **edges** and leaves the middle spacing wider. By pinning down the edges, the entire "rug" (function) stays perfectly flat and smooth, minimizing the error everywhere.

### The "Exactness" (Why it wins the contest?)
The assignment says "half the functions are polynomials".
-   If you have a polynomial $y = x^2 + 5x$ (degree 2) and you give me $n=3$ points...
-   **Chebyshev Interpolation** finds the **unique** polynomial of degree 2 that passes through those points. It literally reconstructs the original math equation. The error is effectively **zero** ($10^{-15}$).
-   Other methods (like Splines) essentially "trace" the curve with small lines or arcs. They will be very close, but never *exact*.

### The "Barycentric" Part (How is it fast?)
Usually, finding a polynomial through $n$ points involves solving a giant matrix (slow, $O(n^3)$).
-   Mathematicians found a shortcut formula called the **Barycentric Formula**.
-   It looks like a weighted average: $g(x) = \frac{\sum \frac{w_i}{x-x_i} y_i}{\sum \frac{w_i}{x-x_i}}$.
-   Because we use special Chebyshev points, we know the weights $w_i$ ahead of time (they are just alternating $1, -1, 1...$).
-   This lets us calculate the answer in one simple loop: **$O(n)$**.

## 4. Fundamental Concept: Global vs. Piecewise

The user asked: *"Is it a part interpolation [small areas] or a big one [whole section]?"*

### Our Choice: Global Interpolation ("The Big One")
We are constructing **one single polynomial** that spans the entire range $[a, b]$.
-   **Math**: $P(x) = a_n x^n + \dots + a_1 x + a_0$.
-   **Visual**: Imagine one stiff but flexible rod curve that passes through every single point simultaneously.
-   **Why?**: If the underlying function is smooth (like a polynomial), a global method captures its "soul" perfectly. It minimizes error exponentially.

### The Alternative: Piecewise Interpolation ("Small Areas")
Methods like **Splines** or **Linear Interpolation** break the range into small chunks (e.g., between $x_1$ and $x_2$, then $x_2$ and $x_3$).
-   **Visual**: Connecting the dots with separate small strings or bent wires.
-   **Why not?**: While safe, it loses the "big picture". It sees a curve as a series of small, unrelated segments. For a true polynomial curve, this approximation is always slightly "off" (the error is $O(h^4)$), whereas the Global method is exact.

### The Special Trick
Usually, Global Interpolation is dangerous because of **Runge's Phenomenon** (wild wiggling at the edges).
-   **Chebyshev Nodes** are the antidote. By clustering points at the ends, they stabilize the global polynomial, giving us the **accuracy of a global method** with the **stability of a piecewise method**.

## 5. Robustness Analysis & Winning Strategy

The user asked: *"Is it going to work well on non-polynomial functions... is there other method that is more accurate?"*

### The "Nasty" Functions (e.g., $f_{11}$ in the image)
The image lists functions like $f_{11}(x) = 2^{1/x^2} \sin(1/x)$.
-   This function oscillates infinitely as $x \to 0$.
-   **No method** (Global or Piecewise) can approximate this well with a finite number of points $n$.
-   **However**, the document explicitly states: *"Functions like 3, 8, 10, 11 will account for at most 4% of the test cases."*

### The "Winning" Probability Calculation
This is a contest. We optimize for the **expected score**.
1.  **Polynomials (~50% of cases)**: Chebyshev is **Exact** (Error $\approx 0$). Splines are merely "okay" (Error $\approx 10^{-5}$). **Winner: Chebyshev.**
2.  **Smooth Non-Polynomials (e.g., $e^x, \sin(x^2)$) (~46% of cases)**: Chebyshev has **Spectral Convergence** (Error decays exponentially, e.g., $10^{-12}$). Splines decay polynomially ($10^{-5}$). **Winner: Chebyshev.**
3.  **Nasty Functions (~4% of cases)**: Both methods will struggle. Splines might look visually "calmer," but the error will still be high.
    -   Since this is only 4% of the grade, we should **not** choose a method (like Splines) that sacrifices accuracy on the 96% just to be slightly safer on the 4%.

### Alternative: Rational Interpolation (Floater-Hormann)
-   **What is it?**: Interpolating with fractions of polynomials ($P(x)/Q(x)$).
-   **Pros**: Better at handling singularities (like $1/x$).
-   **Cons**: Much harder to implement, higher constant overhead ($\approx O(n^2)$ setup unless careful), and often less stable than Barycentric Chebyshev for simple polynomials.
-   **Verdict**: Not worth the risk given the 50% polynomial guarantee.

### Conclusion
**Chebyshev is the statistical winner.** It provides the highest possible score for 96% of the expected test corpus.

## 6. Detailed Design: Barycentric Interpolation

### Algorithm
1.  **Preprocessing (`__init__` or `interpolate` setup)**:
    - Determine $N = n$ (use max points allowed).
    - Calculate Chebyshev Nodes $x_k$ in $[-1, 1]$.
        - We prefer **Chebyshev Roots** (First Kind) or **Extrema** (Second Kind).
        - Roots: $x_k = \cos\left(\frac{2k+1}{2N}\pi\right)$ for $k=0 \dots N-1$. (Avoids endpoints, strictly inside).
        - Extrema: $x_k = \cos\left(\frac{k\pi}{N-1}\right)$. (Includes endpoints).
        - *Decision*: Roots are often safer to avoid potential endpoint singularities if $f$ is undefined exactly at boundary (though problem says closed range), but Extrema are better for bounding error at edges. Given "closed range [a,b]", Extrema (Second Kind) are standard for closed interval interpolation (Clenshaw-Curtis).
    - Map $x_k$ to domain $[a, b]$: $\hat{x}_k = \frac{a+b}{2} + \frac{b-a}{2}x_k$.
    - Sample $y_k = f(\hat{x}_k)$.
    - Compute Barycentric Weights $w_k$.
        - For Chebyshev nodes of 2nd kind, $w_k = (-1)^k \delta_k$, where $\delta_k = 0.5$ for endpoints, $1$ otherwise.
        - For Chebyshev roots (1st kind), $w_k = (-1)^k \sin(\theta_k)$. Or simplified forms exist.

2.  **Interpolation Function `g(x)`**:
    - Use the **Barycentric Formula of the Second Form**:
      $$ g(x) = \frac{\sum_{k=0}^{n-1} \frac{w_k}{x - x_k} y_k}{\sum_{k=0}^{n-1} \frac{w_k}{x - x_k}} $$
    - **Handling $x = x_k$**: If $x$ is extremely close to a node $x_k$, the terms go to infinity. The limit is $y_k$. Implementation must check `if x in nodes: return y`.

3.  **Complexity**:
    - **Setup**: Calculating nodes/weights and sampling $f$: $O(n)$.
    - **Evaluation**: The sum loop is $O(n)$.
    - Matches the "O(n)" requirement.

### Edge Cases
- $n=1$: Cannot form higher degree. Return constant $f((a+b)/2)$.
- $a=b$: Return $f(a)$.

## 7. Challenge: Can we be Adaptive?

The user asked: *"Isn't there a way to combine or know something about the results... so maybe we can choose?"*

### The "Sample-First" Dilemma
To choose the best method (Spline vs. Polynomial), we need to know what the function "looks like" (smooth? jagged? singular?).
1.  **To know the look**, we must sample it (spend our `n` calls).
2.  **The Catch**: The *location* of the samples determines the available methods.
    -   **Splines**: Work best with **Uniformly Spaced** points.
    -   **Global Polynomials**: Require **Chebyshev (Non-Uniform)** points to avoid explosion.

### The Problem
-   If we sample **Uniformly** to start: We validly enable Splines, but we **destroy** the ability to do Global Polynomial interpolation (Runge's phenomenon prevents it). We lose the "Exact" score for polynomials.
-   If we sample **Chebyshev** to start: We enable Global Polynomials (our winner). We *could* fit a Spline through these clustered points, but Splines on highly non-uniform grids are often poor/unstable compared to uniform ones.

### The "Blind" Date
We have to choose our grid (Uniform vs. Chebyshev) **before** we see a single value of $f(x)$. Since we must commit to the grid, and the Chembysev grid is the only one that wins the "Exact Polynomial" category (50% of grade), we are mathematically forced to commit to it.

### Verification is Impossible
We cannot "check our answer" because checking requires calling $f(x)$ at a *new* test point to see if we are close. That would cost $n+1$ calls, which is **forbidden** ($>n$).

## 8. Optimization: Pre-calculated Canonical Nodes (Lookup Table)

The user asked: *"Can we pre-calculate ... for different n ... and adjust to real [a,b]?"*

### Concept: The Canonical Interval $[-1, 1]$
Chebyshev nodes always follow a specific pattern on the range $[-1, 1]$.
-   Formula: $z_k = \cos(\frac{k\pi}{n-1})$.
-   This calculation involves expensive trigonometry (`cos`, `pi`, division).

### The Optimization Strategy
Since $n \le 100$ is small and likely to repeat (testing many functions with $n=10, 20, 50, 100$):
1.  **Lazy Caching**: Inside `Assignment1`, we maintain a cache dictionary `self.cache = {}`.
2.  **Key**: The number of points `n`.
3.  **Value**: A tuple `(z_nodes, weights)` calculated for the canonical interval $[-1, 1]$.
4.  **Runtime**:
    -   When `interpolate(..., n)` is called, check if `n` is in cache.
    -   If yes: Retrieve `z` and `w` ($O(1)$).
    -   If no: Compute and store ($O(n)$).
5.  **Adjustment**: Map the cached $z$ to real $x$ using a simple linear transform:
    $$ x_k = \frac{a+b}{2} + \frac{b-a}{2} z_k $$
    This is extremely fast (vectorized multiplication/addition).

### Benefit
-   **Speed**: Removes the trigonometric overhead from the `interpolate` call, making the setup phase near-instantaneous for repeated `n`.
-   **Simplicity**: Keeps the code clean while handling the user's specific request for "embedded calculations".

## 9. Implementation Plan
1.  Define `interpolate` method.

2.  Handle $n=1$ separately.
3.  Generate Chebyshev nodes (mapped).
4.  Sample $f$.
5.  Define the closure/inner function `wrapper(x)` that implements the Barycentric formula using the captured arrays ($x_k, y_k, w_k$).
6.  Return `wrapper`.
