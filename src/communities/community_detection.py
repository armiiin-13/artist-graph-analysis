from cdlib import algorithms
from collections import Counter
import networkx as nx
from collections import defaultdict

from src.graph.genre_utils import get_macrogenres_for_set

def get_communities(graph):
    return algorithms.lfm(graph, alpha=1.0, weight="weight")

def print_communities(communities):
    print("Comunidades detectadas:", len(communities.communities))

    for i, community in enumerate(communities.communities):
        print(f"Comunidad {i}: {len(community)} artistas")

    memberships = Counter(
        artist
        for community in communities.communities
        for artist in community
    )

    overlapping = {
        artist: count
        for artist, count in memberships.items()
        if count > 1
    }

    print("Artistas en varias comunidades:", len(overlapping))
    print(overlapping)

def louvain_communities(graph):
    communities = nx.community.louvain_communities(
        graph,
        weight="weight",
        resolution=1.0,
        seed=42
    )

    print("Comunidades:", len(communities))
    print("Tamaños:", [len(c) for c in communities])

    for i, community in enumerate(communities):
        print(f"\nComunidad {i + 1} ({len(community)} artistas):")
        print(", ".join(sorted(community)))

    return communities

def leiden_communities(graph):
    communities = algorithms.leiden(graph, weights="weight")

    print("Comunidades:", len(communities.communities))
    print("Tamaños:", [len(c) for c in communities.communities])

    for i, community in enumerate(communities.communities):
        print(f"\nComunidad {i + 1} ({len(community)} artistas):")
        print(", ".join(sorted(community)))

    return communities

def DPclus_communities(graph):
    communities = algorithms.dpclus(
        graph,
        weights="weight",
        d_threshold=0.8,
        cp_threshold=0.5,
        overlap=True
    )

    sizes = sorted(
        [len(c) for c in communities.communities],
        reverse=True
    )

    memberships = Counter(
        artist
        for community in communities.communities
        for artist in community
    )

    print("Comunidades:", len(sizes))
    print("Tamaños:", sizes)
    print("Artistas en varias comunidades:",
          sum(n > 1 for n in memberships.values()))
    print("Artistas sin comunidad:",
          graph.number_of_nodes() - len(memberships))

    for i, community in enumerate(communities.communities, start=1):
        print(f"\nComunidad {i} ({len(community)} artistas):")
        print(", ".join(sorted(community)))

    return communities.communities

def macrogenres_communities(graph):
    macro_communities = defaultdict(set)

    for artist, data in graph.nodes(data=True):
        macrogenres = get_macrogenres_for_set(data["genres"])

        for macro in macrogenres:
            macro_communities[macro].add(artist)

    for macro, artists in macro_communities.items():
        print(f"\n{macro} ({len(artists)} artistas):")
        print(", ".join(sorted(artists)))