__author__ = 'ewaandrejczuk'

import sqlite3

db = sqlite3.connect("data.db")
db.isolation_level = None
cursr = db.cursor()

Article_Ids=[]
cursr.execute('''select article_id, true_quality from articles''')
Articles = cursr.fetchall()

#store the list of articles
for i in Articles:
    Article_Ids.append(i[0])

initial=[0]*len(Article_Ids)
Averages = {Article_Ids[n]: initial[n] for n in range(len(Article_Ids))}

for i in Article_Ids:
        listOfOpinions=[]
        cursr.execute('''select opinion_value from opinions_art_beta where article_id=?''', (i,))

        for k in cursr.fetchall():
             listOfOpinions.append(k[0])
            
        #print listOfOpinions
        suma = float(sum(listOfOpinions))
        #print suma
        average = suma/len(listOfOpinions)
        Averages[i]=average

print Averages

