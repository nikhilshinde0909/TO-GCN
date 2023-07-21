#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import pairwise_distances

## Define help
def print_help():
    print("Usage: python Cutoff.py  <TF expression matrix> <mRNAs expression matrix>")
    print("Identify Pearson's correlation coefficient cutoff values.")

# Check if help flag is present
if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
    print_help()
    sys.exit(0)

# Check if correct number of arguments is provided
if len(sys.argv) != 3:
    print("Invalid number of arguments!")
    print_help()
    sys.exit(1)


df1 = sys.argv[1]
df2 = sys.argv[2]



# Read the inputs
df1 = pd.read_table(df1, index_col=0)
df2 = pd.read_table(df2, index_col=0)


# Function to calculate the observed correlation coefficient between two rows while handling NaNs
def calculate_observed_pcc(row1, row2):
    valid_indices = ~(np.isnan(row1) | np.isnan(row2))
    return pearsonr(row1[valid_indices], row2[valid_indices])[0]

# Function to perform permutation tests to estimate null distribution of correlation coefficients
def permutation_test(row1, row2, num_permutations=1000):
    observed_pcc = calculate_observed_pcc(row1, row2)
    concatenated_rows = np.concatenate((row1, row2))
    permuted_pccs = []

    for _ in range(num_permutations):
        np.random.shuffle(concatenated_rows)
        permuted_row1 = concatenated_rows[:len(row1)]
        permuted_row2 = concatenated_rows[len(row1):]
        permuted_pcc = calculate_observed_pcc(permuted_row1, permuted_row2)
        permuted_pccs.append(permuted_pcc)

    permuted_pccs = np.array(permuted_pccs)
    positive_cutoff = np.percentile(permuted_pccs, 95)  # Set 95th percentile as positive cutoff
    negative_cutoff = np.percentile(permuted_pccs, 5)   # Set 5th percentile as negative cutoff

    return positive_cutoff, negative_cutoff

# Call the function to estimate positive and negative cutoffs
positive_cutoff, negative_cutoff = permutation_test(df1.iloc[0], df2.iloc[0])

print("Positive Cutoff:", positive_cutoff)
print("Negative Cutoff:", negative_cutoff)
