__author__ = 'ewaandrejczuk'
#rom __future__ import division

import numpy as np
from numpy import matrix
from numpy import linalg as LA


print 'Choose the simulation '
print '0 EigenTrust Simple non-distributed '
print '1 EigenTrust Basic non-distributed '

SimulationType=int(raw_input(""))
if(SimulationType==0):
    #number of peers for simulation
    Dimension=int(raw_input("Insert dimension"))
    B =np.random.randint(5, size=(Dimension, Dimension))
    print B


    #A = matrix( [[0,3,1,0],[1,0,4,7],[2,-1,0,-1],[-5,4,3,0]])
    #B= np.matrix('0 3 1 0; 1 0 4 7; 2 -1 0 -1 ;-5 4 3 0')
    MatrixNormal=np.identity(Dimension)
    print 'Matrix Sij ='
    print MatrixNormal

    # Normalizing Local Trust Values

    for i in range(len(B)):
        for j in range(len(B)):
            value=max((B[i,j]),0)
            B[i,j]=value
    print B

    for i in range(len(B)):
        for j in range(len(B)):
            C=B.sum(axis=1) # sum of fields
        #print C
            NumberOfFields=int(C[i])
            if C[i]==0:
                print ' Simple '
            else:
                value=int(B[i,j])
                valueForNormalMatrix=value/NumberOfFields
                #print valueForNormalMatrix
            MatrixNormal[i,j]= float(valueForNormalMatrix)


    #Generate Trust Vector
    e= np.empty(Dimension)
    matrix(e.fill(1/Dimension))

    print 'Trust Vector e =',e
    print "Matrix Normal "
    print MatrixNormal

    Delta=1
    t=e.T
    print 'Vector t',t
    Ct=MatrixNormal.transpose()
    print 'Matrix Ct'
    print Ct
    while (Delta>0.0000001):
     	t2=np.dot(Ct,t)
     	#print'Vector t multiplied =' , t2
     	print 'Vector sum t2 =',t2.sum(axis=0)
     	RestaVectores=t2-t
     	Delta=LA.norm(RestaVectores)
     	print'Delta=',Delta
     	t=t2

    print 'Last Delta',Delta
    print 'Vector t2 final', t2.sum(axis=0)

if (SimulationType==1):

    #Total number of peers

    Dimension=int(raw_input("Insert number of peers: "))
    a=float(raw_input("Insert level of trust for peers: "))

    #Generate Matrix Sij
    B=np.random.randint(-Dimension,Dimension, size=(Dimension, Dimension))

    #Change diagonal = 0
    for i in range(len(B)):
        for j in range(len(B)):
            if (i==j):
                B[i,j]=0
        print B
    #A = matrix( [[0,3,1,0],[1,0,4,7],[2,-1,0,-1],[-5,4,3,0]])

    MatrixNormal=np.identity(Dimension)
    #print 'Matriz Sij ='
    #print MatrixNormal
    print 'Matrix Si,j'
    print B

    #Generate Vector p<----------
    p= np.empty(Dimension)
    matrix(p.fill(1/Dimension))

    print 'Trust vector p =',p

    #Look for fields with sum=0 and change them to trust vector
    for i in range(len(B)):
        for j in range(len(B)):
            C=B.sum(axis=1)
            if C[i]==0:
                B[i]=p
                print B

    # Normalizing Local Trust Values

    for i in range(len(B)):
        for j in range(len(B)):
            C=B.sum(axis=1)
       		#print C
            NumberOfFields=int(C[i])
            value=int(B[i,j])
            valueForNormalMatrix=value/NumberOfFields
            MatrixNormal[i,j]= float(valueForNormalMatrix)


    print "Matrix Normal "
    print MatrixNormal

    #Comienza iteracion
    Delta=1
    t=p.T
    print 'Vector t',t
    Ct=MatrixNormal.transpose()
    print 'Matrix Ct'
    print Ct
    while (Delta>0.0000001):
        t2=np.dot(Ct,t)
        t2=np.dot((1-a),t2)+np.dot(a,p)
        RestaVectores=t2-t
        print 'The rest of vectors =',RestaVectores
        Delta=LA.norm(RestaVectores)
        #print'Delta=',Delta
        t=t2

    print 'LAst Delta',Delta
    print 'Vector t2 final sum: ', t2.sum(axis=0)
    print 'Trust Vector Final :',t2
