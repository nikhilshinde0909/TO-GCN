#!/usr/bin/env python

import sys
import pandas as pd
import networkx as nx
from pyvis.network import Network

## Define help
def print_help():
    print("Usage: python TO-GCN.py  <C1+/C1- co-expression matrix> <Positve/Negative cufoff> <source node> <output prefix>")
    print("Writes time orderded levels and graph for TFs based on PCC cutoff values.")

# Check if help flag is present
if len(sys.argv) == 5 and sys.argv[1] in ['-h', '--help']:
    print_help()
    sys.exit(0)

# Check if correct number of arguments is provided
if len(sys.argv) != 5:
    print("Invalid number of arguments!")
    print_help()
    sys.exit(1)
    
# Read dataframe
df = sys.argv[1]
# Edge cutoff value (choose your desired threshold)
edge_cutoff = float(sys.argv[2])
# Starting node for BFS 
starting_node = str(sys.argv[3])
# Output Prefix
out_pref=sys.argv[4]

# Create the DataFrame
df = pd.read_table(df, sep='\t')

# Create a graph from the dataframe
G = nx.from_pandas_edgelist(df, 'TF', 'Target', edge_attr='PCC')

# Run BFS on the graph to get all edges without depth limit
print("Applying BFS on nodes...")
bfs_tree_edges = nx.bfs_edges(G, source=starting_node)

# Create a new BFS tree graph with edge attributes up to the cutoff depth
bfs_tree = nx.Graph()
for u, v in bfs_tree_edges:
    depth = nx.shortest_path_length(G, source=starting_node, target=v)
    if depth > edge_cutoff:
        bfs_tree.add_edge(u, v, weight=G[u][v]['PCC'])

# Group the nodes by BFS level
node_groups = {}
for node, level in nx.shortest_path_length(bfs_tree, source=starting_node).items():
    if level not in node_groups:
        node_groups[level] = []
    node_groups[level].append(node)

# Save the BFS tree as a table (DataFrame)
result_mat = {
    'TF': [],
    'Target': [],
    'PCC': [],
    'Levels in GCN': []
}

for u, v, data in bfs_tree.edges(data=True):
    result_mat['TF'].append(u)
    result_mat['Target'].append(v)
    result_mat['PCC'].append(data['weight'])
    result_mat['Levels in GCN'].append(nx.shortest_path_length(bfs_tree, source=starting_node)[v])

result_table = pd.DataFrame(result_mat)

# Save the DataFrame as a CSV file
result_table.to_csv(out_pref+'-bfs_levels.TSV', sep='\t', index=False)

# Create a new Pyvis network
net = Network(bgcolor= '#ffffff', neighborhood_highlight=True)

# Add nodes to the network
for level, nodes in node_groups.items():
    for node in nodes:
        net.add_node(node, label=f"{node}", title=f"Level: {level+1}")
        
# Add edges to the network
for u, v, data in bfs_tree.edges(data=True):
    weight = data['weight']
    net.add_edge(u, v, value=weight)
    
# Save graph    
net.save_graph(out_pref+"-bfs_graph.html")    
print("All done thanks for using TO-GCN.py...")
