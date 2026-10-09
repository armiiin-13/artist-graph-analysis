from src.graph.build_graph import generate_graph, Node, Edge
import networkx as nx
import pandas as pd

CENTRALITY_PATH = '../outputs/centrality.csv'
BETWEENEESS_PATH = '../outputs/betweenness.csv'
CLOSENESS_PATH = '../outputs/closeness.csv'
EIGENVECTOR_PATH = '../outputs/eigenvector.csv'
STRENGTH_PATH = '../outputs/strength.csv'

def networkx_graph():
    nodes, edges = generate_graph()
    G = nx.Graph()

    # Add nodes
    for node in nodes:
        G.add_node(node.name, color=node.color)

    for edge in edges:
        G.add_edge(edge.node_1, edge.node_2, color=edge.color)

    return G

def export_csv(data, path):
    df = pd.DataFrame(data=data, index=[0])
    df = df.T
    df.to_csv(path)

def centrality(graph):
    centrality = nx.degree_centrality(graph)
    export_csv(centrality, CENTRALITY_PATH)

def betweenness(graph):
    betweenness = nx.betweenness_centrality(graph, weight='lambda_factor')
    export_csv(betweenness, BETWEENEESS_PATH)

def closeness(graph):
    closeness = nx.closeness_centrality(graph, distance='lambda_factor')
    export_csv(closeness, CLOSENESS_PATH)

def eigenvector(graph):
    eigenvector = nx.eigenvector_centrality(graph, weight='lambda_factor')
    export_csv(eigenvector, EIGENVECTOR_PATH)

def strength(graph):
    strength = dict(graph.degree(weight="weight"))
    export_csv(strength, STRENGTH_PATH)

def export_graph_measures():
    graph = networkx_graph()
    centrality(graph)
    betweenness(graph)
    eigenvector(graph)
    closeness(graph)
    strength(graph)