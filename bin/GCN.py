#!/usr/bin/env python

import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances

## Define help
def print_help():
    print("Usage: python GCN.py <Positive correlation cutoff> <Negative correlation cutoff> <TF expression matrix> <mRNAs expression matrix> <output_prefix>")
    print("Computes Pearson's correlation coefficient between TF and mRNAs.")

# Check if help flag is present
if len(sys.argv) == 5 and sys.argv[1] in ['-h', '--help']:
    print_help()
    sys.exit(0)

# Check if correct number of arguments is provided
if len(sys.argv) != 6:
    print("Invalid number of arguments!")
    print_help()
    sys.exit(1)


# Read file paths from command line arguments
cutoff1 = float(sys.argv[1])
cutoff2 = float(sys.argv[2])
df1 = sys.argv[3]
df2 = sys.argv[4]
out_pref = str(sys.argv[5])
# Read the inputs
df1 = pd.read_table(df1, index_col=0)
df2 = pd.read_table(df2, index_col=0)
df1 = df1[~(df1 == 0).all(axis=1)]
df2 = df2[~(df2 == 0).all(axis=1)]

# Standardize the data
scaler = StandardScaler()
df1_scaled = pd.DataFrame(scaler.fit_transform(df1), columns=df1.columns)
df2_scaled = pd.DataFrame(scaler.transform(df2), columns=df2.columns)

# Calculate pairwise distances
distances = 1 - pairwise_distances(df1_scaled, df2_scaled, metric='correlation')


# Create DataFrame with results
results = pd.DataFrame(distances, index=df1.index, columns=df2.index)
results.index.name = 'TF'
results.columns.name = 'Target'

# Reset index and melt DataFrame
results.reset_index(inplace=True)
results = results.melt(id_vars='TF', var_name='Target', value_name='PCC')

# Filter positive and negative correlations
positive_regulated = results[results['PCC'] > cutoff1]
negative_regulated = results[results['PCC'] < cutoff2]

# Get top correlations in each category
#positive_regulated = positive_regulated.groupby('TF').apply(lambda x: x.nlargest(num_targets, 'PCC')).reset_index(drop=True)
#negative_regulated = negative_regulated.groupby('TF').apply(lambda x: x.nsmallest(num_targets, 'PCC')).reset_index(drop=True)


# Write results as a table
positive_regulated.to_csv(out_pref+'C1+.TSV', sep='\t', index=False)
negative_regulated.to_csv(out_pref+'C1-.TSV', sep='\t', index=False)

## Print thanks
print("Thanks for using GCN.py")
