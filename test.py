__author__ = 'ewaandrejczuk'
import numpy as np
import networkx as nx
from math import isnan
from Graph import *

def from_matrix_to_graph(matrix):
   graph = nx.DiGraph()
   for (x,y), value in np.ndenumerate(matrix):
       if not isnan(value):
           graph.add_edge(x, y, {'weight': value})
   return graph

matrix=np.array([[np.NaN, 0.2, 0.2, np.NaN],[0.3, np.NaN, 0.5, np.NaN],[1, 0.9, np.NaN, 0.1],[np.NaN, 0.5, np.NaN, np.NaN]])
print matrix


GraphG=from_matrix_to_graph(matrix)

for i in range(matrix.shape[0]):
    print i
    duoa1=NewDijsktra(GraphG,i)
    print "dupa1"
    print duoa1


