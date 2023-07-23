"""Create NetworkX graph from data in csv file."""
import os
import pandas as pd
import networkx as nx

from get_data import fetch_ged, parse_ged

def get_graph():
    """Create NetworkX graph from data in csv file."""
    # get file path
    file_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(file_path, '..', 'data')
    # check if csv file exists
    if not os.path.isfile(data_path + 'royal92.csv'):
        # fetch gedcom file
        fetch_ged()

        # parse gedcom file and save data to csv
        parse_ged()

    # read csv file
    df = pd.read_csv(data_path + 'royal92.csv')

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
