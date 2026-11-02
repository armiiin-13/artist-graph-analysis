from src.communities.community_detection import print_communities, leiden_communities, macrogenres_communities
from src.graph.build_graph import generate_graph
from src.graph.networkx_graph import export_graph_measures, networkx_graph
from src.graph.pyvis_graph import pyvis_graph
from src.data.export_data import export
from src.communities.community_detection import get_communities
from src.communities.community_detection import DPclus_communities

graph = networkx_graph()
macrogenres_communities(graph)
