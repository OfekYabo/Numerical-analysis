"""
In this assignment you should interpolate the given function.
"""

import numpy as np
import time
import random


class Assignment1:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        starting to interpolate arbitrary functions.
        """
        self.cache = {
            10: (np.array([ 1.                , 0.9396926207859084, 0.766044443118978 , 0.5000000000000001, 0.1736481776669304,-0.1736481776669303,-0.4999999999999998,-0.7660444431189779,-0.9396926207859083,-1.                ]), np.array([ 0.5,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-0.5])),
            20: (np.array([ 1.                , 0.9863613034027223, 0.9458172417006346, 0.8794737512064891, 0.7891405093963936, 0.6772815716257411, 0.5469481581224269, 0.4016954246529695, 0.2454854871407992, 0.0825793454723324,-0.0825793454723323,-0.2454854871407989,-0.4016954246529694,-0.546948158122427 ,-0.6772815716257409,-0.7891405093963935,-0.879473751206489 ,-0.9458172417006347,-0.9863613034027223,-1.                ]), np.array([ 0.5,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-0.5])),
            50: (np.array([ 1.                , 0.9979453927503363, 0.9917900138232462, 0.9815591569910653, 0.9672948630390295, 0.9490557470106686, 0.9269167573460217, 0.9009688679024191, 0.8713187041233894, 0.8380881048918406, 0.8014136218679566, 0.7614459583691345, 0.7183493500977277, 0.6723008902613168, 0.6234898018587336, 0.5721166601221697, 0.5183925683105252, 0.4625382902408352, 0.4047833431223938, 0.3453650544213078, 0.2845275866310324, 0.2225209339563144, 0.1595998950333795, 0.0960230259076819, 0.0320515775716553,-0.0320515775716552,-0.0960230259076818,-0.1595998950333792,-0.2225209339563143,-0.2845275866310323,-0.3453650544213075,-0.4047833431223937,-0.4625382902408351,-0.518392568310525 ,-0.5721166601221698,-0.6234898018587335,-0.6723008902613168,-0.7183493500977275,-0.7614459583691342,-0.8014136218679565,-0.8380881048918406,-0.8713187041233892,-0.900968867902419 ,-0.9269167573460216,-0.9490557470106685,-0.9672948630390295,-0.9815591569910653,-0.991790013823246 ,-0.9979453927503363, -1.                ]), np.array([ 0.5,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-0.5])),
            100: (np.array([ 1.                , 0.9994965423831851, 0.9979866764718844, 0.9954719225730846, 0.9919548128307953, 0.9874388886763943, 0.9819286972627067, 0.975429786885407 , 0.9679487013963562, 0.9594929736144974, 0.9500711177409454, 0.9396926207859084, 0.9283679330160727, 0.9161084574320696, 0.9029265382866213, 0.8888354486549235, 0.8738493770697849, 0.8579834132349771, 0.8412535328311812, 0.8236765814298328, 0.8052702575310586, 0.7860530947427875, 0.7660444431189781, 0.7452644496757547, 0.7237340381050702, 0.7014748877063213, 0.6785094115571322, 0.6548607339452851, 0.6305526670845225, 0.6056096871376666, 0.5800569095711983, 0.5539200638661104, 0.5272254676105024, 0.5000000000000001, 0.4722710747726827, 0.4440666126057742, 0.4154150130018864, 0.3863451256931286, 0.3568862215918719, 0.3270679633174218, 0.2969203753282749, 0.2664738136900351, 0.2357589355094273, 0.2048066680651908, 0.1736481776669306, 0.1423148382732851, 0.1108381999010111, 0.0792499568567884, 0.0475819158237424,  0.0158659638348082,-0.015865963834808 ,-0.0475819158237423,-0.0792499568567885,-0.110838199901011 ,-0.142314838273285 ,-0.1736481776669303,-0.2048066680651905,-0.2357589355094269,-0.266473813690035 ,-0.2969203753282748,-0.3270679633174214,-0.3568862215918718,-0.3863451256931285,-0.4154150130018865,-0.4440666126057741,-0.4722710747726826,-0.4999999999999998,-0.5272254676105025,-0.5539200638661103,-0.580056909571198 ,-0.6056096871376665,-0.6305526670845225,-0.654860733945285 ,-0.6785094115571321,-0.7014748877063214,-0.7237340381050702,-0.7452644496757547,-0.7660444431189779,-0.7860530947427873,-0.8052702575310586,-0.8236765814298327,-0.8412535328311811,-0.8579834132349768,-0.8738493770697849,-0.8888354486549234,-0.9029265382866211,-0.9161084574320695,-0.9283679330160725,-0.9396926207859082,-0.9500711177409454,-0.9594929736144974,-0.9679487013963562,-0.975429786885407 ,-0.9819286972627066,-0.9874388886763943,-0.9919548128307953,-0.9954719225730846,-0.9979866764718843, -0.9994965423831851,-1.                ]), np.array([ 0.5,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-1. , 1. ,-0.5])),
        }

    def interpolate(self, f: callable, a: float, b: float, n: int) -> callable:
        """
        Interpolate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the interpolation error.
        Your secondary objective is minimizing the running time. 
        The assignment will be tested on variety of different functions with 
        large n values. 
        
        Interpolation error will be measured as the average absolute error at 
        2*n random points between a and b. See test_with_poly() below. 

        Note: It is forbidden to call f more than n times. 

        Note: This assignment can be solved trivially with running time O(n^2)
        or it can be solved with running time of O(n) with some preprocessing.
        **Accurate O(n) solutions will receive higher grades.** 
        
        Note: sometimes you can get very accurate solutions with only few points, 
        significantly less than n. 
        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        n : int
            maximal number of points to use.

        Returns
        -------
        The interpolating function.
        """
        
        if n == 1:
            return lambda x: f((a + b) / 2)

        def get_cheb_canonical(N):
            # Check cache first
            if N in self.cache:
                return self.cache[N]
                
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
            
            self.cache[N] = (z, weights)
            return z, weights

        # Attempt to use n points with vectorization
        z_nodes, weights = get_cheb_canonical(n)
        
        # Map z from [-1, 1] to [a, b]
        nodes = (b - a) / 2 * z_nodes + (a + b) / 2
        
        used_n = n
        
        try:
            # Vectorization attempt (consumes 1 invocation)
            res = f(nodes)
            
            # Verify result format
            if np.isscalar(res):
                y_values = np.full(n, res)
            elif np.shape(res) == (n,):
                y_values = np.array(res)
            else:
                raise ValueError("Shape mismatch or invalid return")
                
        except Exception:
            # Fallback: Vectorization failed. We used 1 invocation.
            # We must proceed with n-1 points to stay within budget.
            used_n = n - 1
            if used_n < 1:
               # Should only happen if input n=1 (handled) or n=1 failed?
               # If input n=2 -> used_n=1.
               pass
            
            # Recompute nodes/weights for n-1
            z_nodes_fallback, weights_fallback = get_cheb_canonical(used_n)
            nodes = (b - a) / 2 * z_nodes_fallback + (a + b) / 2
            weights = weights_fallback
            
            y_values = np.zeros(used_n)
            for i in range(used_n):
                y_values[i] = f(nodes[i])

        self.nodes = nodes
        self.y_values = y_values
        self.weights = weights

        def result(x):
            diff = x - nodes
            
            # Check for exact node match
            close_mask = np.abs(diff) < 1e-14
            if np.any(close_mask):
                return y_values[np.argmax(close_mask)]
            
            t = weights / diff
            numerator = np.dot(t, y_values)
            denominator = np.sum(t)
            
            # Avoid division by zero in rare cases outside interval (shouldn't happen with Cheb 2nd)
            if denominator == 0:
                return 0 # Or closest node
                
            return numerator / denominator

        return result


##########################################################################


import unittest
from functionUtils import *
# from tqdm import tqdm


class TestAssignment1(unittest.TestCase):

    def test_with_poly(self):
        T = time.time()

        ass1 = Assignment1()
        mean_err = 0

        d = 30
        for i in range(100):
            a = np.random.randn(d)

            f = np.poly1d(a)

            ff = ass1.interpolate(f, -10, 10, 100)

            xs = np.random.random(200)
            err = 0
            for x in xs:
                yy = ff(x)
                y = f(x)
                err += abs(y - yy)

            err = err / 200
            mean_err += err
        mean_err = mean_err / 100

        T = time.time() - T
        print(T)
        print(mean_err)

    def test_with_poly_restrict(self):
        ass1 = Assignment1()
        a = np.random.randn(5)
        f = RESTRICT_INVOCATIONS(10)(np.poly1d(a))
        ff = ass1.interpolate(f, -10, 10, 10)
        xs = np.random.random(20)
        for x in xs:
            yy = ff(x)

if __name__ == "__main__":
    unittest.main()
