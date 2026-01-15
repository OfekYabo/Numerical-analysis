# Project Interactions and Dependencies

The 5 parts of the project are interconnected. Success in later assignments often relies on robust implementations of earlier ones.

## Dependency Map

### **Assignment 3 (Integration) -> Uses Assignment 2 (Roots)**
- **Strength**: **Critical**
- **Explanation**: To calculate the "Area Between Two Curves", you must first find the bounds of integration, which are defined by the intersection points of the functions.
- **Impact**: If `intersections()` (Ass2) misses a root or returns an inaccurate point, the integration limits will be wrong, leading to **large errors** in the calculated area.

### **Assignment 3 (Integration) -> Potentially Uses Assignment 1 (Interpolation)**
- **Strength**: **Strong (Heuristic)**
- **Explanation**: Complex functions that are hard to integrate directly might be replaced by a high-accuracy polynomial interpolation (using Ass1 methodology) which is easier to integrate analytically or numerically (e.g. Clenshaw-Curtis quadrature which uses Chebyshev nodes).

### **Assignment 5 (Shape Fitting) -> Uses Assignment 3/4 Concepts**
- **Strength**: **Conceptual / Moderate**
- **Explanation**: 
    - Fitting a 2D shape likely involves optimization techniques similar to 1D Curve Fitting (Ass4).
    - Calculating the area of the fitted shape corresponds to the Integration task (Ass3).
    - While code reuse might not be enforced by imports, the *logic* is cumulative.

### **General Utilities**
- **Commons & FunctionUtils**: Shared files containing `AbstractShape`, sample generators, and decorators interact with all assignments. Changes here affect the entire project.

## Recommendations for Integration
1. **Reuse Code**: When implementing Assignment 3, directly import and use your `Assignment2` class to find intersections. Do not rewrite root finding logic.
2. **Robustness**: Ensure Assignment 2 filters duplicate roots effectively, as `scipy.integrate` or manual integration loops will fail or double-count regions if bounds are duplicated.
3. **Performance**: Assignment 5 is time-critical. If it relies on integration (Ass3), the integration method must be extremely fast, possibly sacrificing a tiny bit of precision for speed if allowed.
