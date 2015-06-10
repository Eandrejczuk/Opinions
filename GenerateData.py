__author__ = 'ewaandrejczuk'
import sqlite3
import random
from faker import Factory
import sys
import scipy

r = 4      #number of reviewers
p = 10     #number of articles
n = 5      #number or articles reviewed by each reviewer - has to be bigger or equal to p/r
o = 3      #average number of opinions for each opinion
ro = r*n     #number of opinions about articles
l2=int(round(p/r,0))      #number of reviews per article

#generate data for reviewers
Results = []
for row in range(0,r):
    if row < int(r/3):
        g=0
    if int(r/3) <= row < int(2*r/3):
        g=1
    if row > int(2*r/3):
        g=2
    Results.append(g)
#print Results

#generate data for articles
GeneratedArticles = [[] for i in range(p)]
fake = Factory.create()
for row in range(0,p):
    if row < int(p/3):
        g=0
    if int(p/3) <= row < int(2*p/3):
        g=1
    if row > int(2*p/3):
        g=2
    GeneratedArticles[row].append(g)
    go=fake.text()
    GeneratedArticles[row].append(go)

print GeneratedArticles


#open database connection
db = sqlite3.connect("data.db")
db.isolation_level = None
cursr = db.cursor()
cursr2 = db.cursor()
cursr3 = db.cursor()

#drop tables if exists
cursr.execute('''drop TABLE if exists reviewers''')
cursr.execute('''drop table if exists rev_img_decode''')
cursr.execute('''drop table if exists articles''')
cursr.execute('''drop table if exists opinions_art''')
cursr.execute('''drop table if exists opinions_op''')

# Create tables
cursr.execute('''CREATE TABLE IF NOT EXISTS reviewers
             (rev_id INTEGER PRIMARY KEY AUTOINCREMENT, self_img_id int)''')

cursr.execute('''CREATE TABLE IF NOT EXISTS rev_img_decode
             (self_img_id INTEGER PRIMARY KEY AUTOINCREMENT, self_img_name text)''')

cursr.execute('''CREATE TABLE IF NOT EXISTS articles
             (article_id INTEGER PRIMARY KEY AUTOINCREMENT, true_quality float, article_title text)''')

cursr.execute('''CREATE TABLE IF NOT EXISTS opinions_art
             (opinion_id INTEGER PRIMARY KEY AUTOINCREMENT, article_id INTEGER NOT NULL, rev_id INTEGER NOT NULL, opinion_value int, opinion_text text,
             FOREIGN KEY(rev_id) REFERENCES reviewers(rev_id),
             FOREIGN KEY(article_id) REFERENCES articles(article_id)
             )''')

cursr.execute('''
             CREATE TABLE IF NOT EXISTS opinions_op
             (article_id INTEGER NOT NULL,
             rev_id integer not null,
             reviewer_of_op integer not null,
             opinion_value int,
             opinion_text text
             )''')

#fill tables with data
for item_r in Results:
    cursr.execute('''INSERT INTO reviewers (rev_id, self_img_id) VALUES (null,?)''', (item_r, ))
for item_a in GeneratedArticles:
    cursr.executemany('''INSERT INTO articles (article_id, true_quality, article_title) VALUES (null,?,?)''', (item_a,))

cursr.execute('''Insert or ignore into rev_img_decode values
             (null, 'low self esteem')''')
cursr.execute('''Insert or ignore into rev_img_decode values
             (null, 'Normal self esteem')''')
cursr.execute('''Insert or ignore into rev_img_decode values
             (null, 'high self esteem')''')

#generate data for opinions
fake2 = Factory.create()
GeneratedOpinions = [[] for i in range(r*n)]
for row in range(0,r*n):
    g=random.randint(1, 10)
    go=fake2.text()
    GeneratedOpinions[row].append(g)
    GeneratedOpinions[row].append(go)
#sample article_id and reviewer_id to create opinion
Reviewers=[]
Articles=[]
listArtRev=[]
initial=[0]*r

cursr2.execute('''select rev_id from reviewers''')
for k in cursr2.fetchall():
    Reviewers.append(k[0])

cursr2.execute('''select article_id from articles''')
for j in cursr2.fetchall():
    Articles.append(j[0])

#dictionary to store number of articles reviewed by each reviewer
NumOfArtForRev = {Reviewers[n]: initial[n] for n in range(len(Reviewers))}
counter=0
#print e
for i in Articles:
    #check if reviewer already checked n articles
    for key, item in NumOfArtForRev.items():
        #if item is item_to_remove:
        if (NumOfArtForRev[key] == n):
            #del some_dict[key]
             del NumOfArtForRev[key]

    los = random.sample(Reviewers, l2)
    for randRev in los:
             d=(i,randRev)
             listArtRev.append(d)
             counter+=1
             if counter >=len(GeneratedOpinions):
                break
             if randRev in NumOfArtForRev:
                NumOfArtForRev[randRev] += 1
    if counter >=len(GeneratedOpinions):
        break

print "size of listArtRev, GeneratedOpinions =", (len(listArtRev),len(GeneratedOpinions))
if  len(listArtRev)   ==  len(GeneratedOpinions):
    Opinions= [list(listArtRev[x])+list(GeneratedOpinions[x]) for x in range(len(listArtRev))]
else:
    print "number or articles reviewed by each reviewer has to be bigger or equal to p/r"
    sys.exit()
#
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,1,9,'excellent')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,2,8,'excellent')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,4,5,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,5,5,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,7,5,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,8,8,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,9,10,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,10,2,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,15,1,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,16,4,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,18,3,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,19,9,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,20,5,'nothing special')''')
# cursr3.execute('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,1,24,5,'nothing special')''')

#insert generated opinions to the database
for item_o in Opinions:
#    print item_o
    cursr3.executemany('''INSERT INTO opinions_art (opinion_id, article_id, rev_id, opinion_value,opinion_text ) VALUES (null,?,?,?,?)''', (item_o, ))



###########################################################################################################################
#opinions of opinions
#print OpinionsOfOp

#match opinions with opinions
cursr2.execute('''select article_id, rev_id from opinions_art''')
ArticleReviewerID = [[] for i in range(len(GeneratedOpinions))]
ArticleReviewerID = cursr2.fetchall()

#self opinions
OpinionsMatched=[]
for i in ArticleReviewerID:
    OpinionsMatched2=(i[0], i[1],i[1])
    OpinionsMatched.append(OpinionsMatched2)

print "opinions matched"
print OpinionsMatched

#list to store reviewers who gave opinion about o opinions already
NumOfOpAboutRevArt = {Reviewers[n]: [0]*r for n in range(len(Reviewers))}

ListRevRev=[]
ListArtRevRev=[]
for article_id in Articles:
    for key, value in NumOfOpAboutRevArt.items():
        #if item is item_to_remove:
        if (NumOfOpAboutRevArt[key] == o):
             #del some_dict[key]
              del NumOfOpAboutRevArt[key]

    cursr2.execute('''select rev_id from opinions_art where article_id=?''', (article_id,))
    temp=[]
    for i in cursr2.fetchall():
         temp.append(i[0])
    for j in temp:
         temp1=temp
         temp1.remove(j)
         if len(temp1)>=o:
             los1 = random.sample(temp1, int(o))
         else:
             los1=temp1
         for randRev in los1:
                  if randRev==j:
                      #j=j-1
                      break
                  d=(article_id,j,randRev)
                  OpinionsMatched.append(d)
                  if randRev in NumOfArtForRev:
                     NumOfArtForRev[randRev] += 1
# print "ListRevRev"
# print ListRevRev
# print len (ListRevRev)

# ArticleRev = [[] for i in range(len(GeneratedOpinions))]
# ArticleRev = cursr2.fetchall()
#
# for l in o:
#     for i in OpinionsIDRev:
#         OpinionsMatched3=(i[0], i[1],i[1])
#         OpinionsMatched.append(OpinionsMatched3)

#opinions about others
#for j in range(0,o):
#     for i in ArticleReviewerID:
#         x=random.choice(RevID)
#         OpinionsMatched2=(i[0],i[1],x)
#         if (OpinionsMatched2 in OpinionsMatched):
#             continue
#         else:
#             OpinionsMatched.append(OpinionsMatched2)

#generate opinions of opinions
fake3 = Factory.create()
OpinionsOfOp = [[] for i in range(len(OpinionsMatched))]
for row in range(0,len(OpinionsMatched)):
    g=random.randint(1, 10)
    go=fake3.text()
    OpinionsOfOp[row].append(g)
    OpinionsOfOp[row].append(go)

#print OpinionsMatched
#print OpinionsOfOp

OpinionsAll= [list(OpinionsMatched[x])+list(OpinionsOfOp[x]) for x in range(len(OpinionsMatched))]

#print OpinionsAll

for item_oo in OpinionsAll:
     #print item_oo
     cursr3.executemany('''INSERT INTO opinions_op (article_id, rev_id, reviewer_of_op, opinion_value,opinion_text)
     VALUES (?,?,?,?,?)''', (item_oo, ))

#cursr.commit()
cursr.close()
cursr2.close()
cursr3.close()

