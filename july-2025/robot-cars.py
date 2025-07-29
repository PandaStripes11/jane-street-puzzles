import numpy as np
from scipy.integrate import dblquad
from scipy.optimize import minimize_scalar

#############################
#        SCIPY CODE         #
#############################
# Low precision, but faster

# Define the weight function
def weight(x, y):
    return (y - x) / (x * y)

# Define the cost functions
def slow_lane_cost(x, y, a):
    return x**2 * weight(x, y)

def fast_lane_cost(x, y, a):
    return (x - a)**2 * weight(x, y)

# Normalization weights (no cost here, just weight contribution)
def slow_lane_weight(x, y):
    return weight(x, y)

def fast_lane_weight(x, y):
    return weight(x, y)

# Compute expected cost for a given a
def expected_cost(a):
    # Numerator: weighted total cost
    slow_cost, _ = dblquad(lambda y, x: slow_lane_cost(x, y, a), 1, a, lambda x: x, lambda x: a)
    fast_cost, _ = dblquad(lambda y, x: fast_lane_cost(x, y, a), a, 2, lambda x: x, lambda x: 2)
    numerator = slow_cost + fast_cost

    # Denominator: total weight over same-lane interactions
    slow_weight, _ = dblquad(lambda y, x: slow_lane_weight(x, y), 1, a, lambda x: x, lambda x: a)
    fast_weight, _ = dblquad(lambda y, x: fast_lane_weight(x, y), a, 2, lambda x: x, lambda x: 2)
    denominator = slow_weight + fast_weight

    return numerator #/ denominator

# Minimize the expected cost over a ∈ (1, 2)
result = minimize_scalar(expected_cost, bounds=(1.111582, 1.111583), method='bounded', options={'xatol': 1e-10})
optimal_a = result.x
min_cost = result.fun

print(optimal_a, min_cost)