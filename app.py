"""Streamlit App for the project."""
import streamlit as st
from plotly import graph_objects as go

from create_graph import get_graph


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
    # check if nodes are selected
    if len(select_nodes) > 0:
        pass
    else:
        # limit nodes from slider
        if num_nodes == 0:
            st.warning('No nodes selected.')
            st.stop()
        elif num_nodes > 100:
            st.warning('Too many nodes selected.')
            st.stop()
        elif num_nodes > 0:
            select_nodes = list(G.nodes())[:num_nodes]

    # get all neighbors of selected nodes
    nodes = []
    neighbors = []
    for node in select_nodes:
        nodes.append(node)
        neighbors.extend(G.neighbors(node))

    # all nodes
    all_nodes = nodes + neighbors

    # get edges from nodes
    edges = G.edges(nodes)

    # create node trace
    node_x = []
    node_y = []

    for node in all_nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',
        marker={
            'size': 15,
        },
        line_width=2
    )

    # add edges to edge trace
    edge_x = []
    edge_y = []

    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

        # create edge trace
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line={'width': 1, 'color': '#888'},
        hoverinfo='none',
        mode='lines'
    )

    # create figure
    fig = go.Figure()

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
