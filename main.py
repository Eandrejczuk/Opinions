__author__ = 'ewaandrejczuk'
import sqlite3
import numpy as np
from math import isnan
import networkx as nx
from Graph import NewDijsktra
import matplotlib.pyplot as plt
from numpy import linalg as LA
from numpy import matrix

def similarity(opinionA, opinionB):
    if (opinionA == 0 or opinionB==0):
        return 0
    else:
        sim=(maxOp-abs(opinionA-opinionB))#/max
        return sim

#Reviewers - list of reviewers
#data - set of opinions about opinions, here article id, reviewer id, reviewer opinion, reviewer of reviewer, opinion about reviewer
def calculate_opinions(Reviewers, data):
    DirectOpinions=np.zeros(shape=(len(Reviewers),len(Reviewers)))
    #print data
    for i in Reviewers:
        for j in data:
            if i==j[0]:
                #print (i, j)
                #do not take into an account self-opinions - to be changed?
                # if j[0]==j[1]:
                #     DirectOpinions[i-1][j[1]-1]=maxOp
                #     continue #calculate values here !!!!
                # else:
                    #DirectOpinions[i-1][j[1]-1]=j[2]
                    DirectOpinions[j[1]-1][i-1]=j[2]
            else:
                continue
    return DirectOpinions

def calculate_S(OpinionsMatrix):
    temp=np.zeros(shape=(len(OpinionsMatrix[0]),len(OpinionsMatrix[0])))
    for i in range(OpinionsMatrix.shape[0]):
        for j in range(OpinionsMatrix.shape[1]):
                if OpinionsMatrix[i][j] > 0:
                    for l in range(OpinionsMatrix.shape[1]):
                        if OpinionsMatrix[i][l]>0: #(j!=l and ):
                            temp[l][j]+=1
                else: continue
    return temp

def normalize_opinions(matrix):
    NormalizedMatrix=np.empty(shape=(len(matrix[0]),len(matrix[0])))
    for y in range(matrix.shape[0]):
        for z in range(matrix.shape[1]):
            if matrix[y][z]==0 or matrix[y][z] is None:
                NormalizedMatrix[y][z] = np.nan
            else:
                value=matrix[y][z]
                NormalizedMatrix[y][z]=value/maxOp

    return NormalizedMatrix

def from_matrix_to_graph(matrix):
   graph = nx.DiGraph()
   for (x,y), value in np.ndenumerate(matrix):
       if not isnan(value):
           graph.add_edge(x, y, {'weight': value})
   return graph

def from_dict_to_matrix(dict):
    matrix=np.empty(len(dict))
    for key, elem in dict.items():
        matrix[key] = elem
    return matrix

def qsort(data):
    if len(data) <= 1:
       return data
    pivot = data[0]
    smaller = []
    greater = []
    for x in data[1:]:
        if x < pivot:
            smaller.append(x)
        else:
            greater.append(x)
    return qsort(greater) + [pivot] + qsort(smaller)
##############################################################################################################################################
#download data from database
if __name__ == "__main__":

    np.set_printoptions(threshold='nan')

    db = sqlite3.connect("data.db")
    db.isolation_level = None
    cursr = db.cursor()

    # cursr.execute('''
    # select max(opinion_value) from opinions_art''')
    # temp = cursr.fetchone()
    # for i in temp:
    #     maxOp=i

    #max opinion about the article
    maxOp = 10

    Articles=[]
    cursr.execute('''select article_id from articles''')
    for k in cursr.fetchall():
        Articles.append(k[0])

    Reviewers=[]
    cursr.execute('''select rev_id from reviewers''')
    for k in cursr.fetchall():
        Reviewers.append(k[0])

    cursr.execute('''
    select article_id, rev_id, opinion_value from opinions_art order by article_id''')
    #article id, reviewer id, reviewer opinion, reviewer of reviewer, opinion about reviewer
    Data_op = cursr.fetchall()

    #create matrix of opinions about articles
    OpinionsMatrix=np.zeros(shape=(len(Articles),len(Reviewers)))

    for i in Articles:
        for j in Data_op:
            if i==j[0]:
                    OpinionsMatrix[i-1][j[1]-1]=j[2]
            else:
                continue
    #print OpinionsMatrix
    #print len(OpinionsMatrix)

    OiOpAll=[]
    #MatrixSim=np.zeros(shape=(len(Articles),len(Reviewers)))
    temp=np.zeros(shape=(len(Reviewers),len(Reviewers)))
    for article_id in Articles:
        cursr.execute('''
        select oa.rev_id, oo.reviewer_of_op,oo.opinion_value from opinions_art oa
        join opinions_op oo on oa.article_id=oo.article_id and oa.rev_id=oo.rev_id
        where oa.article_id=?
        order by oa.rev_id
        ''', (article_id,))
        #reviewer id, reviewer opinion, reviewer of reviewer, opinion about reviewer
        Data = cursr.fetchall()

        #print Data
        #create matrix for direct opinions
        OiOp= calculate_opinions(Reviewers, Data)
        #print "this is OiOp"
        #print OiOp
        #iterate on every element of matrix of opinions about opinions
        #print OiOp
        for y in range(OiOp.shape[0]):
            for z in range(OiOp.shape[1]):
                value = OiOp[y][z]
                #check if opinion about opinion exists
                if (value == 0 and y!=z):
                    k=OpinionsMatrix[article_id-1][z]
                    m=OpinionsMatrix[article_id-1][y]
                    if (k>0 and m>0):
                            temp = similarity(k,m) #add average
                            OiOp[y][z]=temp
                    else:
                        continue
                else:
                    continue
                    #print OiOp
        OiOpAll.append(OiOp)
    #print OiOpAll[0]
    E=np.array((len(Reviewers),len(Reviewers)))
    for i, value in enumerate(OiOpAll):
        if i==0:
             E=OiOpAll[i]
        elif i>=1:
             E=E+OiOpAll[i]
    print "this is OiOpAll"
    print OiOpAll[0]


    S=calculate_S(OpinionsMatrix)
    #print "this is E"
    #print E
    #print S
    with np.errstate(invalid='ignore'):
        MatrixH=np.where(S>0, E/S, 0)

    #print MatrixH
    #print OiOp
    MatrixHNormalized=normalize_opinions(MatrixH)
    GraphG=from_matrix_to_graph(MatrixHNormalized)

    #USE THIS TO PRINT A GRAPH
    #print GraphG.nodes()

    #print GraphG.edges(data = True)

    #dupa = ((u,v) for u,v,d in GraphG.edges_iter(data=True) if d['weight']==1)
    #for i in dupa:
    #    print i
    #pos=nx.spring_layout(GraphG)
    #edge_labels=dict([((u,v,),d['weight'])
    #                 for u,v,d in GraphG.edges(data=True)])
    #node_labels = {node:node for node in GraphG.nodes()};
    #nx.draw_networkx_labels(GraphG, pos, labels=node_labels)
    #nx.draw_networkx_edge_labels(GraphG,pos,edge_labels=edge_labels)
    #nx.draw_networkx(GraphG, pos,node_color='#A0CBE2',edge_color='#404040',width=4,edge_cmap=plt.cm.Blues,with_labels=True)
    #plt.savefig("graph.png", dpi=500, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches=None, pad_inches=0.1)
    #plt.show(GraphG)

    #run Dijkstra for matrix X normalized
    A=np.zeros(shape=(len(GraphG), len(GraphG)))
    for i in range(MatrixHNormalized.shape[0]):
        temp=NewDijsktra(GraphG,i)
        #print temp
        A[i]=from_dict_to_matrix(temp)

    #if opinion exists, take the value, otherwise take the Dijkstra value
    FinalMatrixC=np.zeros((len(Reviewers),len(Reviewers)))
    for y in range(MatrixHNormalized.shape[0]):
            for z in range(MatrixHNormalized.shape[1]):
                if MatrixHNormalized[y][z]>0:
                    FinalMatrixC[y][z]=MatrixHNormalized[y][z]
                else:
                    FinalMatrixC[y][z]=A[y][z]
    #print FinalMatrixC

    print "this is Final Matrix C \n", FinalMatrixC

    print "with mean: ", np.mean(FinalMatrixC, axis=1)

    #not needed - normalising step
    #for i in range(FinalMatrixC.shape[0]):
    #    FinalMatrixC[i] = FinalMatrixC[i]/FinalMatrixC[i].sum()

    print "this is Final Matrix C with normalization for Eigentrust \n", FinalMatrixC
    #Generate Trust Vector
    e= np.empty(len(FinalMatrixC))
    matrix(e.fill(float(1)/len(FinalMatrixC)))
    #print "with sum: ", np.sum(FinalMatrixC, axis=0)

    print 'Trust Vector e =',e

    Delta=1
    t=e.T
    print 'Vector t',t
    Ct=FinalMatrixC.transpose()
    print 'Matrix Ct'
    print Ct

    while (Delta>0.0001):
        t2=np.dot(Ct,t)
        #normalise values
        t2=t2/t2.sum()
        print'Vector t multiplied =' , t2
        print 'Vector sum t2 =',t2.sum(axis=0)
        VectorsRest=t2-t
        #print "vectors rest ", VectorsRest
        Delta=LA.norm(VectorsRest)
        print'Delta=',Delta
        t=t2

    print 'Last Delta',Delta
    print 'Vector t2 final', t2.sum(axis=0)
    print OpinionsMatrix
    OpinionAboutArticle=[]
    for i in range(0, len(Articles)):
            # for j in range(len(Reviewers)):
            #     if OpinionsMatrix[i][j]>0:
            #         OpinionAboutArticle[i][j]=1
            # print OpinionAboutArticle
            reviews = OpinionsMatrix[i]>0
            a = OpinionsMatrix[i]*reviews
            b = t2*reviews
            prod = np.dot(a,b)/b.sum()
            OpinionAboutArticle=OpinionAboutArticle+[prod]

    OpinionAboutArticleSorted= qsort(OpinionAboutArticle)

    print OpinionAboutArticle
    #OpinionAboutArticle[i]=OiOpAll[i]




    #print NewDijsktra2(GraphG,1)
    # for i in range(MatrixHNormalized.shape[0]):
    #     #pass
    #     print i
    #     dupa=NewDijsktra(GraphG,i)
    #     print dupa
    #
    #
    # for i in range(MatrixHNormalized.shape[0]):
    #     #pass
    #     print i
    #     dupa=NewDijsktra(GraphG,i)
    #     print dupa
    #NodesClean = {k: NodesWithNan[k] for k in NodesWithNan if not isnan(NodesWithNan[k])}
    #print MatrixHNormalized
    #for i in range(MatrixHNormalized.shape[0]):

        #for j in range(MatrixHNormalized.shape[1]):
            #MatrixCij= NewDijsktra(MatrixHNormalized[i],i)

    #print MatrixCij
    #print nx.dijkstra_path(Z,0,11)

    #with np.errstate(invalid='ignore'):

    # for y in range(E.shape[0]):
    #     for z in range(E.shape[1]):
    #         value = E[y][z]
    #         #check if opinion about opinion exists
    #         if (value == 0 and y!=z):
    #             for article_id in Articles:
    #                 k=OpinionsMatrix[article_id-1][z]
    #                 m=OpinionsMatrix[article_id-1][y]

#    n = 0
#    H=[]
#    Q=[]


#    for i in range(0,len(Data_op)):
#        for j in range(0, len(Data_op[i])):
#                H[Data_op[i][j]] = n
#                Q[n] = Data_op[i][j]
#                n+=1

#print Cij






