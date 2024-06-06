import numpy as np

from src.algebra import adjust_corr_matrix

size = 10

np.random.seed(42)

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors ** 2).sum(axis=0))

print()
print("VECTORS")
print(vectors.round(3))
print((vectors ** 2).sum(axis=0))

corr = vectors.T @ vectors
print()
print("CORR")
print(corr.round(3))

ls = np.linalg.eigvalsh(corr)
print()
print("LAMBDAS")
print(ls)

target_corr = corr.copy()
i, j, v = 2, 3, 0.9
target_corr[i, j] = target_corr[j, i] = v
corr_fixed = adjust_corr_matrix(corr, i, j, v)

print()
print("TARGET CORR")
print(target_corr.round(3))

ls = np.linalg.eigvalsh(target_corr)
print()
print("TARGET LAMBDAS")
print(ls)

print()
print("FIXED CORR")
print(corr_fixed.round(3))
print("-" * 50)
print(corr.round(3))
print("-" * 50)
print(np.round(corr_fixed - corr, 3))

ls = np.linalg.eigvalsh(corr_fixed)
print()
print("FIXED LAMBDAS")
print(ls)
