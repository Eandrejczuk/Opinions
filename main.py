__author__ = 'ewaandrejczuk'
import sqlite3
import numpy as np
import ModifiedDijkstra as dijkstra

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
                if j[0]==j[1]:
                    continue #calculate values here !!!!
                else:
                    DirectOpinions[i-1][j[1]-1]=j[2]
                    #temp[i-1][j[1]-1]+=1
            else:
                continue
    return DirectOpinions
    #with np.errstate(invalid='ignore'):
    #    CijDirect=np.where(temp>0, DirectOpinions/temp, 0)
    #return CijDirect

def calculate_S(OpinionsMatrix):
    temp=np.zeros(shape=(len(OpinionsMatrix[0]),len(OpinionsMatrix[0])))
    for i in range(OpinionsMatrix.shape[0]):
        for j in range(OpinionsMatrix.shape[1]):
                if OpinionsMatrix[i][j] > 0:
                    #k=OpinionsMatrix[i][j]
                    for l in range(OpinionsMatrix.shape[1]):
                        if (j!=l and OpinionsMatrix[i][l]>0):
                            #m=OpinionsMatrix[i][l]
                            temp[l][j]+=1
                            #temp[j][m]+=1
                else: continue
    return temp

##############################################################################################################################################
#download data from database
if __name__ == "__main__":

    np.set_printoptions(threshold='nan')

    db = sqlite3.connect("data.db")
    db.isolation_level = None
    cursr = db.cursor()

    cursr.execute('''
    select max(opinion_value) from opinions_art''')
    temp = cursr.fetchone()
    for i in temp:
        maxOp=i

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
        #print "dupa"
        #print OiOp
        #print OpinionsMatrix[article_id-1]
        #print OiOpAll
        #iterate on every element of matrix of opinions about opinions
        for y in range(OiOp.shape[0]):
            for z in range(OiOp.shape[1]):
                value = OiOp[y][z]
                #check if opinion about opinion exists
                if (value == 0 and y!=z):
                    k=OpinionsMatrix[article_id-1][z]
                    m=OpinionsMatrix[article_id-1][y]
                    if (k>0 and m>0):
                            temp = similarity(k,m)
                            OiOp[y][z]=temp
                    else:
                        continue
                else:
                    continue
                    #print OiOp
        OiOpAll.append(OiOp)

    E=np.array((len(Reviewers),len(Reviewers)))
    for i, value in enumerate(OiOpAll):
        #print "i"


        #print i
        if i==0:
             E=OiOpAll[i]
             #print "this is E"
             #print E
        elif i>=1:
             E=E+OiOpAll[i]


    #print OiOpAll[0]

    #print E
    S=calculate_S(OpinionsMatrix)

    print E[0]
    print S[0]

    with np.errstate(invalid='ignore'):
         Cij=np.where(S>0, E/S  , 0)

#    n = 0
#    H=[]
#    Q=[]


#    for i in range(0,len(Data_op)):
#        for j in range(0, len(Data_op[i])):
#                H[Data_op[i][j]] = n
#                Q[n] = Data_op[i][j]
#                n+=1

#print Cij




#for i in range(Cij.shape[0]):
#    for j in range(Cij.shape[1]):
#            if Cij[i][j] >1:
#                print Cij[i][j]
#print Cij

#filename = open("outputfile",'w')
#sys.stdout = filename
#print OiOpAll


#print MatrixSim

# cursr.execute('''
# select article_id, rev_id, opinion_value from opinions_art
# order by article_id
# ''')
# #article id, reviewer id, reviewer opinion, reviewer of reviewer, opinion about reviewer
# Data_op = cursr.fetchall()
#
#
#
#
# DirectOpinions=np.zeros(shape=(len(Reviewers),len(Reviewers)))

#for i in Articles:
#    calculate_opinions(Reviewers, Data)

#DirectOpinions=np.zeros(shape=(len(Reviewers),len(Reviewers)))
#temp=np.zeros(shape=(len(Reviewers),len(Reviewers)))

# #direct opinions
# for i in Reviewers:
#     for j in data:
#         if i==j[1]:
#             #do not take into an account self-opinions - to be changed for proper algorithm
#             if j[1]==j[3]:
#                 pass #calculate values here !!!!
#             else:
#                 DirectOpinions[i-1][j[3]-1]+=j[4]
#                 temp[i-1][j[3]-1]+=1
#         else:
#             pass
#
# with np.errstate(invalid='ignore'):
#     CijDirect=np.where(temp>0, DirectOpinions/temp, 0)



#for index,value in np.ndenumerate(CijDirect):
#    if value == 0:
#        print CijDirect[index]


#
# OpinionsMatrix=np.zeros(shape=(len(Articles),len(Reviewers)))
#
# for i in Articles:
#     for j in Data_op:
#         if i==j[0]:
#                 OpinionsMatrix[i-1][j[1]-1]=j[2]
#         else:
#             pass

#print OpinionsMatrix

#print CijDirect
#print OpinionsMatrix[0]

#for i in range (0, len(CijDirect)):
    #if CijDirect[0][i] == 0:
        #print OpinionsMatrix[0][i]



#dupa=[]
#for i in Reviewers:
#    for j in OpinionsMatrix[i-1]:
        #print j
#            dupa.append(j)
#            print dupa
            #print list(itertools.combinations(dupa,2))

# for i in Reviewers:
#     for cell in OpinionsMatrix[i-1].flat:
#             for j in itertools.combinations(OpinionsMatrix[i-1], 2):
#                 print i
#             print cell

#print OpinionsMatrix
#print dist_out

#for cell in dist_out.flat:
#       if cell!= 0:
 #          pass
            #print cell
            #print cell[1][5]
#print len(dist_out)

