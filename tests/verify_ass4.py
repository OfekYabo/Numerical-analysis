
import sys
import numpy as np
import time
sys.path.append('Ass3')
from assignment4 import Assignment4

def sample_poly(x):
    return 2*x**2 - 3*x + 1

def noisy_poly(x):
    return sample_poly(x) + np.random.normal(0, 0.1)

print("Starting custom test...")
ass4 = Assignment4()
fit_func = ass4.fit(noisy_poly, 0, 10, d=2, maxtime=5)

test_x = np.array([0, 5, 10])
true_y = sample_poly(test_x)
fitted_y = np.array([fit_func(x) for x in test_x])

print(f"True Y: {true_y}")
print(f"Fitted Y: {fitted_y}")
mse = np.mean((true_y - fitted_y)**2)
print(f"MSE: {mse}")

if mse < 0.1:
    print("SUCCESS: Fit is good.")
else:
    print("FAILURE: Fit is poor.")
