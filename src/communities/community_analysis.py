from src.graph.build_graph import generate_graph
from collections import Counter

from src.graph.genre_utils import get_macrogenres_for_set


def community_analysis(communities):
    nodes, _ = generate_graph()
    nodes_dict = {node.name: node for node in nodes}

    for i, community in enumerate(communities, start=1):
        macrogenres = Counter()

        for artist in community:
            node = nodes_dict[artist]
            macrogenres.update(get_macrogenres_for_set(node.genres))

        n = sum(macrogenres.values())

        print(f"\nComunidad {i} ({len(community)} artistas):")

        for genre, count in macrogenres.most_common():
            print(f"  {genre}: {count / n * 100:.2f}%")