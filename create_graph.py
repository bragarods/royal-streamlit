"""Create NetworkX graph from data in csv file."""
import pandas as pd
import networkx as nx

# read csv file
df = pd.read_csv('data/royal92.csv')

# create graph
G = nx.Graph()

# add nodes
for i, row in df.iterrows():
    G.add_node(
        row['pointer'],
        name=row['name'],
        first=row['first'],
        last=row['last'],
        birth=row['birth'],
        death=row['death'],
        mother=row['mother'],
        father=row['father']
        )

# print # of nodes
print(f'Number of nodes: {G.number_of_nodes()}')
