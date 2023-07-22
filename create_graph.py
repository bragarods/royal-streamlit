"""Create NetworkX graph from data in csv file."""
import pandas as pd
import networkx as nx

def get_graph():
    """Create NetworkX graph from data in csv file."""
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
    print(f'# of nodes added: {G.number_of_nodes()}')

    # add edges
    for i, row in df.iterrows():
        G.add_edge(row['pointer'], row['mother'])
        G.add_edge(row['pointer'], row['father'])

    # print # of edges
    print(f'# of edges added: {G.number_of_edges()}')

    # position nodes
    pos = nx.spring_layout(G)

    # return graph
    return G, pos
