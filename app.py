"""Streamlit App for the project."""
import streamlit as st
import networkx as nx
from plotly import graph_objects as go

from get_data import fetch_ged, parse_ged
from create_graph import get_graph

# fetch and parse gedcom file
fetch_ged()
parse_ged()

# load graph and positions
@st.cache_data
def load_graph():
    """Load graph and positions."""
    return get_graph()

# load graph and positions
G, pos = load_graph()

# set page title
st.title('Royal Family Graph')

# set page subtitle
st.markdown('''
    This is a graph of the British Royal Family.
    ''')

# set page description
st.markdown('''
    The graph was created using data from the
    [Royal92 dataset] from the [Gedcom Project].
    ''')

# set page footer
st.markdown('''
    [Royal92 dataset]:  http://www.gedcom.org/royalty.html
    [Gedcom Project]:   http://www.gedcom.org/
    ''')

# set page sidebar
st.sidebar.title('Sidebar')

# set page sidebar description
st.sidebar.markdown('''
    This is the sidebar.
    ''')

# set page sidebar footer
st.sidebar.markdown('''
    This is the sidebar footer.
    ''')

# set page sidebar checkbox
show_graph = st.sidebar.checkbox(
    'Show Graph',
    value=True
    )

# set page sidebar slider
num_nodes = st.sidebar.slider(
    'Number of Nodes',
    min_value=0,
    max_value=G.number_of_nodes(),
    value=10,
    step=1
    )

# set page sidebar multiselect
select_nodes = st.sidebar.multiselect(
    'Select Nodes',
    G.nodes()
    )

# create plot
if show_graph:
    # create figure
    fig = go.Figure()

    # limit nodes from slider
    if num_nodes == 0:
        st.warning('No nodes selected.')
        st.stop()
    elif num_nodes > 100:
        st.warning('Too many nodes selected.')
        st.stop()
    elif num_nodes > 0:
        nodes = list(G.nodes())[:num_nodes]

    # get edges from nodes
    edges = G.edges(nodes)

    # create node trace
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker={
            'size': 10,
            'line_width': 2
        }
    )

    # create edge trace
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line={'width': 0.5, 'color': '#888'},
        hoverinfo='none',
        mode='lines'
    )

    # add nodes to node trace
    for node in nodes:
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    # add edges to edge trace
    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    # add hover text to node trace
    for node, adjacencies in enumerate(G.adjacency()):
        node_info = f'{adjacencies[0]} - # of connections: {len(adjacencies[1])}'
        node_trace['text'] += tuple([node_info])

    # add node trace to figure
    fig.add_trace(node_trace)

    # add edge trace to figure
    fig.add_trace(edge_trace)

    # update layout
    fig.update_layout(
        title='Royal Family Graph',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin={"b": 20, "l": 5, "r": 5, "t": 40},
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False}
    )

    # show figure
    st.plotly_chart(fig, use_container_width=True)
