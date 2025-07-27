import numpy as np
from scipy.integrate import dblquad
from scipy.optimize import minimize_scalar

############################
#       MPMATH CODE        #
############################
# Higher precision

from mpmath import mp, quad

# Set desired precision (50 decimal places)
mp.dps = 21

# Define the original weight function
def weight(x, y):
    return (y - x) / (x * y)

# Wrap the weight function to accept a dummy third parameter (for a)
def weight_wrapped(x, y, a=None):
    return weight(x, y)

# Slow lane cost integrand
def slow_cost_integrand(x, y, a):
    return x**2 * weight(x, y)

# Fast lane cost integrand
def fast_cost_integrand(x, y, a):
    return (x - a)**2 * weight(x, y)

# Manual double integration using mpmath
def double_integral(func, x_min, x_max, y_min_func, y_max_func, a):
    def outer_integral(x):
        def inner_integral(y):
            return func(x, y, a)
        return quad(inner_integral, [y_min_func(x), y_max_func(x)])
    return quad(outer_integral, [x_min, x_max])

# High-precision expected cost function
def expected_cost_high_precision(a_val):
    a = mp.mpf(a_val)
    one, two = mp.mpf(1), mp.mpf(2)

    # Slow lane: 1 <= x < y <= a
    slow_cost = double_integral(slow_cost_integrand, one, a, lambda x: x, lambda x: a, a)
    slow_weight = double_integral(weight_wrapped, one, a, lambda x: x, lambda x: a, a)

    # Fast lane: a < x < y <= 2
    fast_cost = double_integral(fast_cost_integrand, a, two, lambda x: x, lambda x: two, a)
    fast_weight = double_integral(weight_wrapped, a, two, lambda x: x, lambda x: two, a)

    return (slow_cost + fast_cost) / (slow_weight + fast_weight)

# Brute-force minimization using high-precision steps
def brute_force_minimize(start=1.111582608, stop=1.111582609, steps=100):
    min_a = None
    min_cost = mp.inf
    for i in range(steps + 1):
        a = mp.mpf(start + (stop - start) * i / steps)
        cost = expected_cost_high_precision(a)
        print(a, cost)
        if cost < min_cost:
            min_cost = cost
            min_a = a
    return min_a, min_cost

# Run it
a_min, cost_min = brute_force_minimize()
print("Minimizer a:", a_min)
print("Minimum expected cost:", cost_min)