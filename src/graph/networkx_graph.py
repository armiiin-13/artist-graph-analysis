from src.graph.build_graph import generate_graph, Node, Edge
import networkx as nx
import pandas as pd

CENTRALITY_PATH = '../outputs/centrality.xlsx'
BETWEENEESS_PATH = '../outputs/betweenness.xlsx'
CLOSENESS_PATH = '../outputs/closeness.xlsx'
EIGENVECTOR_PATH = '../outputs/eigenvector.xlsx'
STRENGTH_PATH = '../outputs/strength.xlsx'

def networkx_graph():
    nodes, edges = generate_graph()
    G = nx.Graph()

    # Add nodes
    for node in nodes:
        G.add_node(node.name, color=node.color)

    for edge in edges:
        G.add_edge(edge.node_1, edge.node_2, color=edge.color)

    return G

def export_xlsx(data, path):
    df = pd.DataFrame(data=data, index=[0])
    df = df.T
    df.to_excel(path)

def centrality(graph):
    centrality = nx.degree_centrality(graph)
    export_xlsx(centrality, CENTRALITY_PATH)

def betweenness(graph):
    betweenness = nx.betweenness_centrality(graph, weight='lambda_factor')
    export_xlsx(betweenness, BETWEENEESS_PATH)

def closeness(graph):
    closeness = nx.closeness_centrality(graph, distance='lambda_factor')
    export_xlsx(closeness, CLOSENESS_PATH)

def eigenvector(graph):
    eigenvector = nx.eigenvector_centrality(graph, weight='lambda_factor')
    export_xlsx(eigenvector, EIGENVECTOR_PATH)

def strength(graph):
    strength = dict(graph.degree(weight="weight"))
    export_xlsx(strength, STRENGTH_PATH)

def export_graph_measures():
    graph = networkx_graph()
    centrality(graph)
    betweenness(graph)
    eigenvector(graph)
    closeness(graph)
    strength(graph)