import time
import numpy as np

def benchmark_matrix_construction(N, d=10):
    # Simulate data
    xs = np.linspace(-1, 1, N)
    ys = np.random.rand(N)
    
    start = time.time()
    
    # Logic copied from Assignment4.fit (approximated for benchmark)
    center = 0
    scale = 1
    zs = (xs - center) / scale
    
    # Precompute powers
    z_pows = np.zeros((2 * d + 1, N))
    z_pows[0] = 1.0
    for k in range(1, 2 * d + 1):
        z_pows[k] = z_pows[k-1] * zs
        
    m_dim = d + 1
    M = np.zeros((m_dim, m_dim))
    v = np.zeros(m_dim)
    
    for i in range(m_dim):
        for j in range(i, m_dim):
            val = np.sum(z_pows[i+j])
            M[i, j] = val
            M[j, i] = val
        v[i] = np.sum(ys * z_pows[i])
        
    end = time.time()
    return end - start

print("Benchmarking Matrix Construction Cost...")
print(f"{'N (Samples)':<15} | {'Time (seconds)':<15}")
print("-" * 35)

for n_test in [1000, 5000, 10000, 20000, 50000]:
    t = benchmark_matrix_construction(n_test)
    print(f"{n_test:<15} | {t:.6f}s")
