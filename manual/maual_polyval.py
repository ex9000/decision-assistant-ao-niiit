import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval

# Example matrix of coefficients for N polynomials of power K
# Each row represents a polynomial's coefficients from lowest to highest degree
polynomials_matrix = np.array(
    [
        [4, -2, 1],  # Polynomial 1: 3 - 2x + x^2
        [-1, 0, 4],  # Polynomial 2: -1 + 4x^2
        [2, 0, -1],  # Polynomial 2: -1 + 4x^2
        # ... Add more rows for more polynomials
    ]
).T

# Example 1D array of M values
values = np.linspace(0, 2)  # Replace with your actual values

# Evaluate each polynomial at all values in the 1D array
results = polyval(values, polynomials_matrix)

fig, ax = plt.subplots(1)
ax.plot(values, results.T)

plt.show()

print(results)
