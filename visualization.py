import plotly.express as px
import plotly.graph_objects as go
import networkx as nx


def apply_premium_dark_theme(fig):
    """Applies DataZone's dark purple/cyan theme to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#BB95DF",
        title_font=dict(size=14, color="#00f2fe", family="Poppins"),
        margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(
            gridcolor='#232338',
            zeroline=False,
            tickfont=dict(color='#a3a3c2'),
            title_font=dict(color='#a3a3c2')
        ),
        yaxis=dict(
            gridcolor='#232338',
            zeroline=False,
            tickfont=dict(color="#a3a3c2"),
            title_font=dict(color="#a3a3c2")
        ),
        legend=dict(font=dict(color="#BB95DF"))
    )
    return fig


def generate_bar_chart(history_df):
    """Shows how many detections happened per crop, from real history."""
    counts = history_df.groupby('crop').size().reset_index(name='Detections')
    fig = px.bar(
        counts,
        x='crop',
        y='Detections',
        color='crop',
        color_discrete_sequence=["#18CA86", '#00f2fe', '#ff4a5a'],
        labels={'crop': 'Crop Species'},
        title="DETECTIONS PER CROP"
    )
    return apply_premium_dark_theme(fig)


def generate_line_chart(history_df):
    """Shows model confidence over the sequence of detections made this session."""
    fig = px.line(
        history_df,
        y='confidence',
        x=history_df.index,
        title="MODEL CONFIDENCE OVER SESSION",
        color_discrete_sequence=['#bf7af0'],
        labels={'x': 'Detection #', 'confidence': 'Confidence (%)'}
    )
    fig.update_traces(line=dict(width=3))
    return apply_premium_dark_theme(fig)


def generate_pie_chart(history_df):
    """Shows the share of detections across crops, from real history."""
    counts = history_df.groupby('crop').size().reset_index(name='Detections')
    fig = px.pie(
        counts,
        names='crop',
        values='Detections',
        color_discrete_sequence=['#1a1a3a', '#bf7af0', '#00f2fe'],
        hole=0.4,
        title="DETECTION SHARE BY CROP"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#ffffff'))
    return apply_premium_dark_theme(fig)


def generate_network_topology():
    """Decorative diagram resembling the CNN's layer routing - illustrative only."""
    G = nx.erdos_renyi_graph(n=8, p=0.45, seed=24)
    pos = nx.circular_layout(G)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='#2d2d54'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[f"CNN_L{i}" for i in G.nodes()],
        textposition="top center",
        textfont=dict(color='#00f2fe', size=10),
        marker=dict(
            showscale=False,
            color="#f50892",
            size=15,
            line_width=2,
            line_color="#0ee3ee"
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title='ILLUSTRATIVE NETWORK LAYER TOPOLOGY',
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    return apply_premium_dark_theme(fig)
