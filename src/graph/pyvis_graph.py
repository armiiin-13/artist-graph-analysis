from src.graph.build_graph  import generate_graph
from pyvis.network import Network

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
    import webbrowser

    html = nt.generate_html(notebook=False)

    with open("../outputs/custom_net.html", "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open("../outputs/custom_net.html")