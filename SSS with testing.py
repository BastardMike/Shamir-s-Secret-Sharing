#!/usr/bin/env python
# coding: utf-8

# In[56]:


import random
from itertools import combinations

# Set the secret
secret = 75

# Function to generate a set of n shares for the given secret
def generate_shares(secret, n, k):
    if k > n:
        raise ValueError("k must be less than or equal to n")
    coefficients = [secret] + [random.randint(0, 100) for _ in range(k-1)]
    shares = []
    for i in range(1, n+1):
        x = i
        y = sum(coefficients[j] * (x ** j) for j in range(k))
        shares.append((x, y))
    return shares

# Function to reconstruct the secret from a set of shares
def reconstruct_secret(shares):
    if len(shares) < 3:
        raise ValueError("At least 3 shares are required to reconstruct the secret")
    x_values, y_values = zip(*shares)
    numerator = 0
    denominator = 0
    for i in range(len(x_values)):
        xi, yi = x_values[i], y_values[i]
        # Calculate the Lagrange coefficient
        li_numerator = li_denominator = 1
        for j in range(len(x_values)):
            if i != j:
                xj = x_values[j]
                li_numerator *= -xj
                li_denominator *= xi - xj
        li = li_numerator / li_denominator
        numerator += li * yi
        denominator += li
    return round(numerator / denominator)

# Generate a set of shares for the secret
shares = generate_shares(secret, n=10, k=5)

# Verify that the secret can only be reconstructed when a sufficient number of shares are combined
for i in range(3, 11):
    for subset in combinations(shares, i):
        try:
            reconstructed_secret = reconstruct_secret(subset)
            if reconstructed_secret != secret:
                print("Error: Incorrectly reconstructed secret")
            else:
                print("Success: Secret correctly reconstructed from %d shares" % i)
                break
        except ValueError as e:
            pass
    else:
        print("Error: Not enough shares to reconstruct the secret")

# Attempt to reconstruct the secret with an insufficient number of shares and verify that it fails
subset = random.sample(shares, 2)
try:
    reconstructed_secret = reconstruct_secret(subset)
    print("Error: Secret should not be reconstructable with only 2 shares")
except ValueError as e:
    print("Success: %s" % str(e))

# Attempt to reconstruct the secret with all 10 shares and verify that it succeeds
try:
    reconstructed_secret = reconstruct_secret(shares)
    if reconstructed_secret != secret:
        print("Error: Incorrectly reconstructed secret")
    else:
        print("Success: Secret correctly reconstructed from all 10 shares")
except ValueError as e:
    print("Error: %s" % str(e))


# In[ ]:




