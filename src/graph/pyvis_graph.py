from src.graph.build_graph  import generate_graph
from pyvis.network import Network
import webbrowser
import math
import base64
from collections import defaultdict

from src.graph.networkx_graph import networkx_graph


def pyvis_graph():
    nodes, edges = generate_graph()

    # Create the net
    nt = Network(
        height="750px",
        width="100%",
        directed=False,
        cdn_resources="in_line"
    )

    for node in nodes:
        nt.add_node(
            node.name,
            label=node.name,
            color=node.color,
            size=15
        )

    for edge in edges:
        nt.add_edge(
            edge.node_1,
            edge.node_2,
            color=edge.color,
            physics=True,
            width=1
        )

    nt.set_options("""
    var options = {
      "edges": {
        "smooth": false
      },
      "interaction": {
        "hideEdgesOnDrag": true,
        "hideNodesOnDrag": false
      },
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "centralGravity": 0.01,
          "springLength": 180,
          "springConstant": 0.02,
          "damping": 0.4,
          "avoidOverlap": 0.5
        },
        "stabilization": {
          "enabled": true,
          "iterations": 300,
          "updateInterval": 25,
          "fit": true
        }
      }
    }
    """)

    # Export Dynamic HTML
    html = nt.generate_html(notebook=False)

    with open("../outputs/custom_net.html", "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open("../outputs/custom_net.html")

def pyvis_graph_communities(nxgraph, communities, path):
    colors = [
        "#4E79A7",
        "#F28E2B",
        "#E15759",
        "#76B7B2",
        "#59A14F",
        "#B07AA1"
    ]

    for i, community in enumerate(communities):
        for node in community:
            nxgraph.nodes[node]["group"] = i
            nxgraph.nodes[node]["color"] = colors[i]

    net = Network(
        height="750px",
        width="100%",
        notebook=False,
        cdn_resources="in_line"
    )

    for node, attrs in nxgraph.nodes(data=True):
        for key, value in attrs.items():
            if isinstance(value, set):
                attrs[key] = list(value)

    net.from_nx(nxgraph)

    for node in net.nodes:
        node["size"] = 15

    for edge in net.edges:
        if nxgraph.nodes[edge["from"]]["group"] == nxgraph.nodes[edge["to"]]["group"]:
            edge["color"] = "#DDDDDD"
            edge["width"] = 1
        else:
            edge["color"] = "#999999"
            edge["width"] = 0.3

    net.set_options("""
    var options = {
      "edges": {
        "smooth": false
      },
      "interaction": {
        "hideEdgesOnDrag": true,
        "hideNodesOnDrag": false
      },
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "centralGravity": 0.01,
          "springLength": 180,
          "springConstant": 0.02,
          "damping": 0.4,
          "avoidOverlap": 0.5
        },
        "stabilization": {
          "enabled": true,
          "iterations": 300,
          "updateInterval": 25,
          "fit": true
        }
      }
    }
    """)

    # Export Dynamic HTML
    html = net.generate_html(notebook=False)

    with open(f"../outputs/{path}.html", "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(f"../outputs/{path}.html")

def create_node_image(colors):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'

    if len(colors) == 1:
        svg += f'<circle cx="50" cy="50" r="48" fill="{colors[0]}"/>'
    else:
        angle = 360 / len(colors)

        for i, color in enumerate(colors):
            start = math.radians(i * angle - 90)
            end = math.radians((i + 1) * angle - 90)

            x1 = 50 + 48 * math.cos(start)
            y1 = 50 + 48 * math.sin(start)
            x2 = 50 + 48 * math.cos(end)
            y2 = 50 + 48 * math.sin(end)

            svg += (
                f'<path d="M 50 50 L {x1} {y1} '
                f'A 48 48 0 0 1 {x2} {y2} Z" '
                f'fill="{color}"/>'
            )

    svg += '</svg>'

    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")

    return f"data:image/svg+xml;base64,{encoded}"


def pyvis_graph_dpclus(nxgraph, communities):
    colors = [
        "#4E79A7", "#F28E2B", "#E15759", "#76B7B2",
        "#59A14F", "#B07AA1", "#EDC948", "#FF9DA7",
        "#9C755F", "#264653", "#E63946", "#8338EC",
        "#FF006E", "#8AC926", "#1982C4", "#FF595E"
    ]

    memberships = defaultdict(set)

    for i, community in enumerate(communities):
        for node in community:
            memberships[node].add(i)

    net = Network(
        height="750px",
        width="100%",
        directed=False,
        notebook=False,
        cdn_resources="in_line"
    )

    # Nodes
    for node in nxgraph.nodes:
        groups = sorted(memberships[node])
        node_colors = [colors[i % len(colors)] for i in groups]

        if not node_colors:
            node_colors = ["#999999"]

        net.add_node(
            node,
            label=str(node),
            shape="image",
            image=create_node_image(node_colors),
            size=15,
            title=(
                f"Comunidades: {', '.join(str(i+1) for i in groups)}"
                if groups else "Sin comunidad"
            )
        )

    # Edges
    for u, v in nxgraph.edges:
        shared = memberships[u] & memberships[v]
        net.add_edge(
            u,
            v,
            color="#999999" if shared else "#CCCCCC",
            width=1 if shared else 0.3,
            physics=True
        )

    net.set_options("""
    var options = {
      "edges": {
        "smooth": false
      },
      "interaction": {
        "hideEdgesOnDrag": true,
        "hideNodesOnDrag": false
      },
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "centralGravity": 0.01,
          "springLength": 180,
          "springConstant": 0.02,
          "damping": 0.4,
          "avoidOverlap": 0.5
        },
        "stabilization": {
          "enabled": true,
          "iterations": 300,
          "updateInterval": 25,
          "fit": true
        }
      }
    }
    """)

    # Export Dynamic HTML
    html = net.generate_html(notebook=False)

    with open("../outputs/dpclus.html", "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open("../outputs/dpclus.html")