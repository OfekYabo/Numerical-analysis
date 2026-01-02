import numpy as np
from assignment1 import Assignment1

def test_cache_integrity():
    ass = Assignment1()
    
    # Formula logic copied from get_cheb_canonical to verify against
    def compute_runtime(N):
        if N == 1:
            return np.array([0.0]), np.array([1.0])
        j = np.arange(N)
        z = np.cos(j * np.pi / (N - 1))
        weights = np.ones(N)
        weights[0] = 0.5
        weights[N - 1] = 0.5
        weights[1::2] = -1 * weights[1::2]
        return z, weights

    print("Verifying Hardcoded Cache Integrity...")
    all_passed = True
    
    for n, (cached_z, cached_w) in ass.cache.items():
        # Compute fresh
        true_z, true_w = compute_runtime(n)
        
        # Compare
        z_match = np.allclose(cached_z, true_z, atol=1e-15)
        w_match = np.allclose(cached_w, true_w, atol=1e-15)
        
        if not z_match or not w_match:
            print(f"FAILED: n={n}")
            print(f"  Nodes match: {z_match}")
            print(f"  Weights match: {w_match}")
            all_passed = False
        else:
            print(f"PASSED: n={n}")

    if all_passed:
        print("\nSUCCESS: All pre-calculated constants match runtime formula exactly.")
    else:
        print("\nFAILURE: Some constants are incorrect.")

if __name__ == "__main__":
    test_cache_integrity()
