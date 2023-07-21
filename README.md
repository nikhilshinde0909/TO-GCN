# TO-GCN
Python pipeline for Time Ordered Gene Co-expression Network analysis

# Execution
Clone latest release of TO-GCN with following command \
```git clone https://github.com/nikhilshinde0909/TO-GCN.git```

# Dependancies
Python==3.10.10 \
Networkx==3.1 \
Pandas==1.5.3 \
Numpy==1.25.0 \
Pyvis==0.3.2 \
Scikit-learn==1.3.0 

# Implementation

Step I: Software installations \
Install python and python modules described above with pip \
for eg.\

```pip install networkx==3.1```

or \
create TO-GCN conda env from file

```conda env create -f TO-GCN.yml```

Step II: Estimate the PCC cutoffs \
Estimate PCC cutoffs by using script Cutoff.py as follows

```python Cutoff.py TF_matrix.TSV All_gene_matrix.TSV```

Step III: Get PCC values for TFs and genes as follows by using GCN.py 

```python GCN.py <positive PCC cutoff> <negative PCC cutoff> TF_matrix.TSV All_gene_matrix.TSV <output prefix>```

this will write <output prefix>-C1+.TSV and <output prefix>-C1-.TSV positively and negatively regulated genes by TFs respectively. 

Step IV: Get time ordered levels for positively and negatively regulated genes using outputs in step II (eg. Rio-C1+.TSV) seed node and PCC cutoff in step I as follows

```python TO-GCN.py Rio-C1+.TSV <postive cutoff> <seed node> <output prefix>```

this will write <output prefix>-bfs_graph.html and <output prefix>-bfs_levels.TSV

# Thanks for using TO-GCN 
