__author__ = 'ewaandrejczuk'
import numpy as np
import networkx as nx
from math import isnan
from Graph import *
from plan import *
import matplotlib.pyplot as plt

def from_matrix_to_graph(matrix):
   graph = nx.DiGraph()
   for (x,y), value in np.ndenumerate(matrix):
       if not isnan(value):
           graph.add_edge(x, y, {'weight': value})
   return graph

matrix=np.array([[1, 0.9, np.NaN, np.NaN, 0.2,np.NaN],
                 [np.NaN, 1, 0.9, np.NaN, 0.4, np.NaN],
                 [np.NaN,np.NaN,1,np.NaN,np.NaN, 0.7],
                 [np.NaN, np.NaN, 0.5,1,np.NaN,np.NaN]
                 ,[np.NaN,np.NaN,np.NaN,np.NaN,1,0.2],
                 [np.NaN,np.NaN,np.NaN,0.4,np.NaN,1]])
print matrix

# matrix=np.array([[np.NaN,0.2    ,np.NaN,np.NaN,0.8],
#                  [np.NaN,np.NaN ,1     ,np.NaN,np.NaN],
#                  [np.NaN,np.NaN ,1     ,np.NaN,np.NaN],
#                  [np.NaN,np.NaN ,np.NaN,1,     np.NaN],
#                  [np.NaN,np.NaN ,np.NaN,0.3,  np.NaN]
#                  ])
# print matrix
GraphG=from_matrix_to_graph(matrix)
# pos=nx.spring_layout(GraphG)
# edge_labels=dict([((u,v,),d['weight'])
#                  for u,v,d in GraphG.edges(data=True)])
# node_labels = {node:node for node in GraphG.nodes()};
# #nx.draw_networkx_labels(GraphG, pos, labels=node_labels)
# nx.draw_networkx_edge_labels(GraphG,pos,edge_labels=edge_labels)
# nx.draw_networkx(GraphG)
# plt.show(GraphG)
# for i in range(matrix.shape[0]):
#     print i
#     duoa1=NewDijsktra(GraphG,i)
#     print "dupa1"
#     print duoa1

import time

t0 = time.time()
dupa1=NewDijsktra(GraphG,1)
t1 = time.time()
print dupa1
print "time = ", t1-t0

t0 = time.time()
dupa2=NewDijsktra2(GraphG,0)
t1 = time.time()

print dupa2
print "time = ", t1-t0



