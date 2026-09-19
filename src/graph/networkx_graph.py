from src.graph.build_graph import generate_graph, Node, Edge
import networkx as nx
import pandas as pd

nodes, edges = generate_graph()
G = nx.Graph()

# Add nodes
for node in nodes:
    G.add_node(node.name, color=node.color)

for edge in edges:
    G.add_edge(edge.node_1, edge.node_2, color=edge.color)

# Centrality
centrality = nx.degree_centrality(G)

df = pd.DataFrame(data=centrality, index=[0])
df = df.T
df.to_excel('../../outputs/centrality.xlsx')

# Betweenness edges value
betweenness = nx.betweenness_centrality(G, weight='lambda_factor')

df = pd.DataFrame(data=betweenness, index=[0])
df = df.T
df.to_excel('../../outputs/betweenness.xlsx')

# Closeness
closeness = nx.closeness_centrality(G, distance='lambda_factor')

df = pd.DataFrame(data=closeness, index=[0])
df = df.T
df.to_excel('../../outputs/closeness.xlsx')

# Eigenvector
eigenvector = nx.eigenvector_centrality(G, weight='lambda_factor')

df = pd.DataFrame(data=eigenvector, index=[0])
df = df.T
df.to_excel('../../outputs/eigenvector.xlsx')

# Strength
strength = dict(G.degree(weight="weight"))

df = pd.DataFrame(data=strength, index=[0])
df = df.T
df.to_excel('../../outputs/strength.xlsx')