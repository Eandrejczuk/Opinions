import numpy

def NewDijsktra(graph, start):
    D = {}  # Reversed distances dict
    B = {}  # Final distances dict
    P = {}  # Predecessor dict
    # Fill the dicts with default values
    for node in graph.nodes():
        D[node] = 10  # Vertices are unreachable
        P[node] = ""  # Vertices have no predecessors
        B[node] = 1
    D[start] = 1  # The start vertex needs no move
    unseen_nodes = list(graph.nodes())  # All nodes are unseen
    while len(unseen_nodes) > 0:
        # Select the node with the lowest value in D (final distance)
        shortest = None
        node = ''
        for temp_node in unseen_nodes:
            if shortest is None:
                shortest = D[temp_node]
                node = temp_node
            elif D[temp_node] < shortest:
                shortest = D[temp_node]
                node = temp_node
        # Remove the selected node from unseen_nodes
        unseen_nodes.remove(node)
        # For each child (ie: connected vertex) of the current node
        for child_node, child_value in graph[node].items():
            if D[child_node] > D[node] / child_value["weight"]:
                D[child_node] = D[node] / child_value["weight"]
                # To go to child_node, you have to go through node
                P[child_node] = node
                B[child_node]=1/D[child_node]

    return B
