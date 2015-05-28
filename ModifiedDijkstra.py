from collections import defaultdict
from heapq import *

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen = [(1,f,())], set()
    while q:
        a= q[0]

        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, ((cost*c), v2, path))
    #return float("inf")

if __name__ == "__main__":
    edges = [
        ("A", "B", 5),
        ("A", "D", 6),
        ("A", "C", 5),
        ("B", "C", 5),
        ("B", "D", 4),
        ("B", "E", 3),
        ("C", "E", 2),
        ("D", "E", 1),
        ("D", "F", 7),
        ("E", "F", 8),
        ("E", "G", 2),
        ("F", "G", 9)
    ]

    print "=== Dijkstra ==="
    print edges
    print "A -> E:"
    print dijkstra(edges, "A", "E")

    #print "F -> G:"
    #print dijkstra(edges, "F", "G")
    #print "A -> F:"
    #print dijkstra(edges, "A", "G")