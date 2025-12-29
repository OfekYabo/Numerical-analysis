import numpy as np

def get_cheb_canonical(N):
    if N == 1:
        return np.array([0.0]), np.array([1.0])
    
    # Chebyshev nodes of the second kind (Extrema) in [-1, 1]
    j = np.arange(N)
    z = np.cos(j * np.pi / (N - 1))
    
    # Barycentric Weights (Chebyshev 2nd kind)
    weights = np.ones(N)
    weights[0] = 0.5
    weights[N - 1] = 0.5
    weights[1::2] = -1 * weights[1::2]
    
    return z, weights

# Add n-1 values for standard test cases
common_ns = [10, 20, 50, 100]
fallback_ns = [n-1 for n in common_ns]
all_ns = sorted(common_ns + fallback_ns)

print("        self.cache = {")
for n in all_ns:
    z, w = get_cheb_canonical(n)
    z_str = np.array2string(z, separator=',', precision=16, max_line_width=1000).replace('\n', '')
    w_str = np.array2string(w, separator=',', precision=16, max_line_width=1000).replace('\n', '')
    
    print(f"            {n}: (np.array({z_str}), np.array({w_str})),")
print("        }")
