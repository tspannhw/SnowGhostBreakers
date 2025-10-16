"""
Neo4j Graph Visualization for Ghost Detection Network
Visualize graph analytics results using Python
Reference: https://neo4j.com/docs/snowflake-graph-analytics/current/visualization/
"""

import snowflake.connector
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple
import numpy as np

class GhostGraphVisualizer:
    """Visualize ghost detection network using graph data"""
    
    def __init__(self, connection_params: Dict):
        """Initialize with Snowflake connection parameters"""
        self.conn = snowflake.connector.connect(**connection_params)
        self.cursor = self.conn.cursor()
        
    def load_graph_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load nodes and edges from Snowflake"""
        # Load nodes
        nodes_query = """
        SELECT node_id, name, type, threat_level, status
        FROM NEO4J_ALL_NODES
        """
        self.cursor.execute(nodes_query)
        nodes_df = self.cursor.fetch_pandas_all()
        
        # Load edges
        edges_query = """
        SELECT source_node, target_node, relationship_type, weight
        FROM NEO4J_ALL_EDGES
        """
        self.cursor.execute(edges_query)
        edges_df = self.cursor.fetch_pandas_all()
        
        return nodes_df, edges_df
    
    def create_networkx_graph(self, nodes_df: pd.DataFrame, 
                            edges_df: pd.DataFrame) -> nx.Graph:
        """Create NetworkX graph from dataframes"""
        G = nx.Graph()
        
        # Add nodes with attributes
        for _, node in nodes_df.iterrows():
            G.add_node(
                node['NODE_ID'],
                name=node['NAME'],
                type=node['TYPE'],
                threat_level=node.get('THREAT_LEVEL', 'Unknown'),
                status=node.get('STATUS', 'Unknown')
            )
        
        # Add edges with weights
        for _, edge in edges_df.iterrows():
            if G.has_node(edge['SOURCE_NODE']) and G.has_node(edge['TARGET_NODE']):
                G.add_edge(
                    edge['SOURCE_NODE'],
                    edge['TARGET_NODE'],
                    relationship=edge['RELATIONSHIP_TYPE'],
                    weight=edge['WEIGHT']
                )
        
        return G
    
    def visualize_network_interactive(self, G: nx.Graph, 
                                     layout: str = 'spring') -> go.Figure:
        """Create interactive network visualization using Plotly"""
        # Calculate layout
        if layout == 'spring':
            pos = nx.spring_layout(G, k=0.5, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G)
        
        # Create edge traces
        edge_traces = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                showlegend=False
            )
            edge_traces.append(edge_trace)
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        
        color_map = {
            'Ghost': '#ff6b6b',
            'Location': '#4ecdc4',
            'Investigator': '#45b7d1',
            'Investigation': '#f7dc6f'
        }
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            node_data = G.nodes[node]
            node_text.append(
                f"<b>{node_data['name']}</b><br>"
                f"Type: {node_data['type']}<br>"
                f"Threat: {node_data.get('threat_level', 'N/A')}<br>"
                f"Connections: {G.degree(node)}"
            )
            
            node_color.append(color_map.get(node_data['type'], '#cccccc'))
            node_size.append(10 + G.degree(node) * 2)
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                color=node_color,
                size=node_size,
                line=dict(width=2, color='white')
            ),
            showlegend=False
        )
        
        # Create figure
        fig = go.Figure(data=edge_traces + [node_trace])
        
        fig.update_layout(
            title='Ghost Detection Network Graph',
            title_font_size=20,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white')
        )
        
        return fig
    
    def visualize_community_detection(self) -> go.Figure:
        """Visualize community detection results"""
        query = """
        SELECT 
            community_id,
            COUNT(*) as member_count,
            COUNT(CASE WHEN type = 'Ghost' THEN 1 END) as ghost_count,
            COUNT(CASE WHEN type = 'Location' THEN 1 END) as location_count
        FROM NEO4J_GHOST_COMMUNITIES
        GROUP BY community_id
        ORDER BY member_count DESC
        """
        self.cursor.execute(query)
        df = self.cursor.fetch_pandas_all()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Ghosts',
            x=df['COMMUNITY_ID'],
            y=df['GHOST_COUNT'],
            marker_color='#ff6b6b'
        ))
        
        fig.add_trace(go.Bar(
            name='Locations',
            x=df['COMMUNITY_ID'],
            y=df['LOCATION_COUNT'],
            marker_color='#4ecdc4'
        ))
        
        fig.update_layout(
            title='Ghost Communities (Louvain Detection)',
            xaxis_title='Community ID',
            yaxis_title='Member Count',
            barmode='stack',
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white')
        )
        
        return fig
    
    def visualize_centrality_ranking(self) -> go.Figure:
        """Visualize PageRank centrality scores"""
        query = """
        SELECT 
            name,
            type,
            pagerank_score,
            degree
        FROM NEO4J_GHOST_PAGERANK
        WHERE type = 'Ghost'
        ORDER BY pagerank_score DESC
        LIMIT 20
        """
        self.cursor.execute(query)
        df = self.cursor.fetch_pandas_all()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['NAME'],
            y=df['PAGERANK_SCORE'],
            marker=dict(
                color=df['DEGREE'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Connections")
            ),
            text=df['DEGREE'],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Importance: %{y:.2f}<br>Connections: %{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Ghost Importance Ranking (PageRank)',
            xaxis_title='Ghost',
            yaxis_title='Importance Score',
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            xaxis_tickangle=-45
        )
        
        return fig
    
    def visualize_hotspot_map(self) -> go.Figure:
        """Visualize location hotspots"""
        query = """
        SELECT 
            name,
            pagerank_score as importance,
            degree as activity_level
        FROM NEO4J_GHOST_PAGERANK
        WHERE type = 'Location'
        ORDER BY pagerank_score DESC
        LIMIT 15
        """
        self.cursor.execute(query)
        df = self.cursor.fetch_pandas_all()
        
        fig = go.Figure(data=[go.Scatter(
            x=df['ACTIVITY_LEVEL'],
            y=df['IMPORTANCE'],
            mode='markers+text',
            marker=dict(
                size=df['ACTIVITY_LEVEL'] * 5,
                color=df['IMPORTANCE'],
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Importance")
            ),
            text=df['NAME'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Activity: %{x}<br>Importance: %{y:.2f}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Paranormal Hotspot Analysis',
            xaxis_title='Activity Level (Connections)',
            yaxis_title='Importance Score',
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white')
        )
        
        return fig
    
    def export_to_neo4j_format(self, output_file: str = 'ghost_graph_export.json'):
        """Export graph data in Neo4j-compatible format"""
        nodes_df, edges_df = self.load_graph_data()
        
        # Convert to Neo4j format
        neo4j_data = {
            'nodes': nodes_df.to_dict('records'),
            'edges': edges_df.to_dict('records')
        }
        
        import json
        with open(output_file, 'w') as f:
            json.dump(neo4j_data, f, indent=2)
        
        print(f"✓ Graph data exported to {output_file}")
    
    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()


def main():
    """Example usage"""
    # Configure connection
    connection_params = {
        'account': 'YOUR_ACCOUNT',
        'user': 'YOUR_USER',
        'password': 'YOUR_PASSWORD',
        'warehouse': 'GHOST_WAREHOUSE',
        'database': 'GHOST_DETECTION',
        'schema': 'APP'
    }
    
    # Create visualizer
    viz = GhostGraphVisualizer(connection_params)
    
    try:
        # Load data
        print("Loading graph data from Snowflake...")
        nodes_df, edges_df = viz.load_graph_data()
        print(f"✓ Loaded {len(nodes_df)} nodes and {len(edges_df)} edges")
        
        # Create NetworkX graph
        print("Creating network graph...")
        G = viz.create_networkx_graph(nodes_df, edges_df)
        print(f"✓ Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Generate visualizations
        print("\nGenerating visualizations...")
        
        # 1. Interactive network
        fig1 = viz.visualize_network_interactive(G, layout='spring')
        fig1.write_html('ghost_network_interactive.html')
        print("✓ Interactive network saved to ghost_network_interactive.html")
        
        # 2. Community detection
        fig2 = viz.visualize_community_detection()
        fig2.write_html('ghost_communities.html')
        print("✓ Community analysis saved to ghost_communities.html")
        
        # 3. Centrality ranking
        fig3 = viz.visualize_centrality_ranking()
        fig3.write_html('ghost_importance_ranking.html')
        print("✓ Importance ranking saved to ghost_importance_ranking.html")
        
        # 4. Hotspot map
        fig4 = viz.visualize_hotspot_map()
        fig4.write_html('paranormal_hotspots.html')
        print("✓ Hotspot analysis saved to paranormal_hotspots.html")
        
        # Export data
        viz.export_to_neo4j_format('ghost_graph_export.json')
        
        print("\n✅ All visualizations generated successfully!")
        print("\nGraph Statistics:")
        print(f"  Nodes: {G.number_of_nodes()}")
        print(f"  Edges: {G.number_of_edges()}")
        print(f"  Density: {nx.density(G):.4f}")
        print(f"  Average Clustering: {nx.average_clustering(G):.4f}")
        
    finally:
        viz.close()


if __name__ == '__main__':
    main()

