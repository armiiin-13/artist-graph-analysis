from src.communities.community_analysis import community_analysis
from src.communities.community_detection import print_communities, leiden_communities, macrogenres_communities, \
    louvain_communities
from src.graph.build_graph import generate_graph
from src.graph.networkx_graph import export_graph_measures, networkx_graph
from src.graph.pyvis_graph import pyvis_graph, pyvis_graph_communities, pyvis_graph_dpclus
from src.data.export_data import export
from src.communities.community_detection import get_communities
from src.communities.community_detection import DPclus_communities

graph = networkx_graph()
# print('Comunidades de Louvain')
# comm = louvain_communities(graph)

# print('Comunidades de Leiden')
# comm = leiden_communities(graph)

print('Comunidades de DPClus')
comm = DPclus_communities(graph)
# pyvis_graph_dpclus(graph, comm)

# print('Comunidad de Macrogéneros')
# macrogenres_communities(graph)

community_analysis(comm)