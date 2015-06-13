__author__ = 'ewaandrejczuk'
import sqlite3
import sys
from scipy.stats import beta
import numpy as np
import random

def standardize_distance(a):
    difference=np.round(a*10,0)
    for i in range(len(difference)):
        if difference[i]==10:
            difference[i]=9
    #print "this is a difference", difference
    return difference

def standardize_quality(a):
    difference=np.round(a*10,0)
    #for i in range(len(difference)):
    if difference==0:
            difference=1
    #print "this is a quality", difference
    return difference

def calculate_opinions_about_art(recommender_distance, true_quality):
    #max1=max(true_quality-1, 10-true_quality)
    #if max1<recommender_distance:
    #    recommender_distance=max1
    temp = true_quality - recommender_distance
    if (temp  <= 10 and temp >0):
        opinion_art = true_quality - recommender_distance
    else:
        opinion_art = true_quality + recommender_distance
    #print opinion_art
    return opinion_art

def calculate_recommender_distance(recommender_distance, true_quality):
    max1=max(true_quality-1, 10-true_quality)
    if max1<recommender_distance:
        final_distance=max1
    else:
        final_distance=recommender_distance
    return final_distance

def check_if_remove_element(dict, value):
    for key, item in dict.items():
        #if item is item_to_remove:
        if (dict[key] == value):
            #del some_dict[key]
            del dict[key]

def check_dict_empty(dict, table, value):
    if dict == {}:
        print "not enough reviewers or articles, total size should be:", len(table) * value
        sys.exit()

# def create_opinion(NumOfArtForRev, z, NumOfOpForArt, y, Articles):
#
#     check_if_remove_element(NumOfArtForRev, z)
#     check_dict_empty(NumOfArtForRev, z)
#     #check if article was checked y times already
#     check_if_remove_element(NumOfOpForArt, y)
#     check_dict_empty(NumOfOpForArt, y)
#
#     rand_rev = random.choice(NumOfArtForRev.keys())
#     rand_art = random.choice(NumOfOpForArt.keys())
#
#     if rand_art in NumOfOpForArt:
#                 NumOfOpForArt[rand_art] += 1
#     if rand_rev in NumOfArtForRev:
#                 NumOfArtForRev[rand_rev] += 1
#
#     #find real quality of selected article
#     if rand_art in Articles:
#         quality = Articles[rand_art]
#
#     real_quality=standardize_quality(quality)
#     opinion_art=calculate_opinions_about_art(i, real_quality)
#
#     elem = (rand_art, rand_rev, opinion_art)




def main():

    ########################################################################################################################
    #This is to generate opinions about articles
    size_good=30
    alpha_good=1.5
    beta_good=8

    size_bad=30
    alpha_bad=8
    beta_bad=1.5

    #n = size_bad + size_good #number of all opinions about articles
    z = 5 # max number of papers for each reviewer
    y = 3 # number of opinions for each paper

    Articles=[]
    Reviewers=[]
    listArtRev=[]
    listTemp=[]

    #distance for good recommenders
    good = beta.rvs(alpha_good, beta_good, size=size_good)
    good_stand = standardize_distance(good)
    #print "mean good recommenders = ", np.mean(good), np.mean(good_stand)
    #print good_stand

    #distance for bad recommenders
    bad = beta.rvs(alpha_bad, beta_bad, size=size_bad)
    bad_stand = standardize_distance(bad)
    #print "mean bad recommenders = ", np.mean(bad), np.mean(bad_stand)
    #print bad_stand

    #open database connection
    db = sqlite3.connect("data.db")
    db.isolation_level = None
    cursr = db.cursor()
    cursr2 = db.cursor()

    Article_Ids=[]
    cursr.execute('''select article_id, true_quality from articles''')
    Articles = cursr.fetchall()

    #store the list of articles
    for i in Articles:
        Article_Ids.append(i[0])

    #create a dictionary from tuple to search for keys easily
    Articles=dict(Articles)
    #print Articles

    #print Article_Ids
    cursr2.execute('''select rev_id from reviewers''')
    for k in cursr2.fetchall():
        Reviewers.append(k[0])
    cursr.execute('''drop table if exists opinions_art_beta''')
    cursr.execute('''drop table if exists opinions_op_beta''')

    cursr.execute('''CREATE TABLE IF NOT EXISTS opinions_art_beta
             (article_id INTEGER NOT NULL, rev_id INTEGER NOT NULL, opinion_value int,
             FOREIGN KEY(rev_id) REFERENCES reviewers(rev_id),
             FOREIGN KEY(article_id) REFERENCES articles(article_id)
             )''')

    cursr.execute('''
             CREATE TABLE IF NOT EXISTS opinions_op_beta
             (article_id INTEGER NOT NULL,
             rev_id integer not null,
             reviewer_of_op integer not null,
             opinion_value int
             )''')
    GoodRev=[]
    BadRev=[]
    for k in Reviewers:
        if k <= len(Reviewers)/2:
            GoodRev.append(k)
        else:
            BadRev.append(k)


    initial1=[0]*len(GoodRev)
    initial2=[0]*len(Article_Ids)

    NumOfArtForGoodRev = {GoodRev[j]: initial1[j] for j in range(len(GoodRev))}
    NumOfOpForArt = {Article_Ids[l]: initial2[l] for l in range(len(Article_Ids))}
    counter=0

    for i in range(len(good_stand)):

        #check if reviewer already checked z articles
        check_if_remove_element(NumOfArtForGoodRev,z)
        check_dict_empty(NumOfArtForGoodRev, GoodRev, z)

        #check if article was checked y times already
        check_if_remove_element(NumOfOpForArt,y)
        check_dict_empty(NumOfOpForArt, Articles, y)

        rand_rev = random.choice(NumOfArtForGoodRev.keys())
        rand_art = random.choice(NumOfOpForArt.keys())

        while (rand_art,rand_rev) in listTemp:
            print (rand_art,rand_rev)
            rand_rev = random.choice(NumOfArtForGoodRev.keys())
            rand_art = random.choice(NumOfOpForArt.keys())

        if rand_art in NumOfOpForArt:
                    NumOfOpForArt[rand_art] += 1
        if rand_rev in NumOfArtForGoodRev:
                    NumOfArtForGoodRev[rand_rev] += 1

        #find real quality of selected article
        if rand_art in Articles:
            quality = Articles[rand_art]

        real_quality=standardize_quality(quality)
        final_distance=calculate_recommender_distance(good_stand[i],real_quality)

        good_stand[i]=final_distance

        opinion_art=calculate_opinions_about_art(final_distance, real_quality)
        elem = (rand_art, rand_rev, opinion_art)
        temp = (rand_art, rand_rev)
        listTemp.append(temp)
        listArtRev.append(elem)
        counter+=1
        #if counter >=n:
        #        break


    initial1=[0]*len(BadRev)

    NumOfArtForBadRev = {BadRev[j]: initial1[j] for j in range(len(BadRev))}

    for i in range(len(bad_stand)):
        #check if reviewer already checked z articles
        check_if_remove_element(NumOfArtForBadRev,z)
        check_dict_empty(NumOfArtForBadRev, BadRev, z)

        #check if article was checked y times already
        check_if_remove_element(NumOfOpForArt,y)
        check_dict_empty(NumOfOpForArt, Articles, y)

        rand_rev = random.choice(NumOfArtForBadRev.keys())
        rand_art = random.choice(NumOfOpForArt.keys())

        while (rand_art,rand_rev) in listTemp:
            #print (rand_art,rand_rev)
            rand_rev = random.choice(NumOfArtForBadRev.keys())
            rand_art = random.choice(NumOfOpForArt.keys())

        if rand_art in NumOfOpForArt:
                    NumOfOpForArt[rand_art] += 1
        if rand_rev in NumOfArtForBadRev:
                    NumOfArtForBadRev[rand_rev] += 1
        #find real quality of selected article
        if rand_art in Articles:
            quality = Articles[rand_art]

        real_quality=standardize_quality(quality)

        final_distance=calculate_recommender_distance(bad_stand[i],real_quality)
        bad_stand[i]=final_distance
        opinion_art=calculate_opinions_about_art(final_distance, real_quality)

        elem = (rand_art, rand_rev, opinion_art)
        temp = (rand_art, rand_rev)
        listTemp.append(temp)
        listArtRev.append(elem)

        counter+=1

    #print "articles: ", NumOfOpForArt
    #print "reviewers good: ", NumOfArtForGoodRev
    #print "reviewers bad: ", NumOfArtForBadRev
    #print listTemp
    print "(article, reviewer, opinion)"
    print listArtRev
    #print len(listArtRev)
    #calculate_opinions_about_art(all, Articles[1])

    # print len(Articles)
    #insert generated opinions to the database
    for item_o in listArtRev:
        #    print item_o
        cursr.executemany('''INSERT INTO opinions_art_beta (article_id, rev_id, opinion_value) VALUES (?,?,?)''', (item_o, ))

    ########################################################################################################################
    #This is to generate opinions about opinions
    distance=np.concatenate((good_stand, bad_stand), axis=0)
    #print distance
    #rint len(distance)


    #print OpinionsOfOp

    #match opinions with opinions
    # ArticleReviewerID = listTemp
    #
    # #self opinions
    # OpinionsMatched=[]
    # k=len(Reviewers)
    # #list to store reviewers who gave opinion about o opinions already
    # #NumOfOpAboutRevArt = {Reviewers[n]: [0]*k for n in range(len(Reviewers))}
    #
    # for article_id in Articles:
    # #    for key, value in NumOfOpAboutRevArt.items():
    # #        #if item is item_to_remove:
    # #        if (NumOfOpAboutRevArt[key] == (y-1)):
    # #             #del some_dict[key]
    # #              del NumOfOpAboutRevArt[key]
    #     count=0
    #     listOfRevOfArt=[]
    #     cursr2.execute('''select rev_id from opinions_art_beta where article_id=?''', (article_id,))
    #
    #     for i in cursr2.fetchall():
    #          listOfRevOfArt.append(i[0])
    #     random.shuffle(listOfRevOfArt)
    #     #print listOfRevOfArt
    #     for j in listOfRevOfArt:
    #          temp1=list(listOfRevOfArt)
    #          temp1.remove(j)
    #
    #          if len(temp1)>(y-1):
    #              los1 = random.sample(temp1, int(y-1))
    #          else:
    #              los1=temp1
    #          for randRev in los1:
    #                   if randRev==j:
    #                       #j=j-1
    #                       break
    #                   d=(article_id,j,randRev)
    #                   OpinionsMatched.append(d)
    #                   count+=1
    #          if (count == y+2):
    #             break
                      #if randRev in NumOfOpAboutRevArt:

    for i in Articles:
        Articles[i]=Articles[i]*10
    print Articles
    print distance
    #   NumOfOpAboutRevArt[randRev] += 1
    # print "(article_id, rev1, rev2)"
    # print OpinionsMatched
    # print len(OpinionsMatched)

    OpinionsAll=[]
    for i in listArtRev:
        listOfRevOfArt=[]
        cursr2.execute('''select rev_id from opinions_art_beta where article_id=?''', (i[0],))

        for k in cursr2.fetchall():
             listOfRevOfArt.append(k[0])
        #print listOfRevOfArt
        listOfRevOfArt.remove(i[1])
        random.shuffle(listOfRevOfArt)
        #temp1=list(listOfRevOfArt)
        for j in listOfRevOfArt:
            if j in GoodRev:
                opinion = 10 - abs(i[2] - Articles[i[0]])
            else:
                opinion=abs(i[2] - Articles[i[0]])
            dupa=(i[0],i[1],j,opinion)
            OpinionsAll.append(dupa)
    print "(article, reviewerArt, opinionArt, reviewerOp, opinionOp)"
    print OpinionsAll

    for item_oo in OpinionsAll:
     print item_oo
     cursr.executemany('''INSERT INTO opinions_op_beta (article_id, rev_id, reviewer_of_op, opinion_value)
     VALUES (?,?,?,?)''', (item_oo, ))

if __name__ == "__main__":
    main()



    # while len(listArtRev)<n:
    #     for i in range(len(Articles)):
    #         #check if reviewer already checked n articles
    #         for key, item in NumOfArtForRev.items():
    #             #if item is item_to_remove:
    #             if (NumOfArtForRev[key] == k):
    #                 #del some_dict[key]
    #                  del NumOfArtForRev[key]
    #
    #
    #         real_quality=standardize_quality(Articles[i][1])
    #         opinion_art=calculate_opinions_about_art(all_distances[i], real_quality)
    #
    #         #if (abs(opinion_art - real_quality) > 7):
    #         #    rand_rev = random.choice(BadRev)
    #         #else:
    #         #    rand_rev = random.choice(GoodRev)
    #         rand_rev = random.choice(Reviewers)
    #         elem = (i, rand_rev, opinion_art)
    #         listArtRev.append(elem)
    #         counter+=1
    #         #if counter >=n:
    #         #        break
    #         if rand_rev in NumOfArtForRev:
    #                 NumOfArtForRev[rand_rev] += 1
    #     if counter >=n:
    #             break



        # for i in bad_stand:
    #     rand_art = random.choice(Articles)
    #     if rand_art[0] in NumOfOpForArt:
    #                 NumOfOpForArt[rand_art[0]] += 1
    #                 if (NumOfOpForArt[rand_art[0]] == y):
    #                     #del some_dict[key]
    #                      del NumOfOpForArt[rand_art[0]]
    #
    #     #print rand_art[1]
    #     real_quality=standardize_quality(rand_art[1])
    #     opinion_art=calculate_opinions_about_art(i, real_quality)
    #     rand_rev = random.choice(BadRev)
    #     elem = (rand_art[0], rand_rev, opinion_art)
    #     listArtRev.append(elem)
    #     counter+=1
    #     #if counter >=n:
    #     #        break
    #     if rand_rev in NumOfArtForGoodRev:
    #                 NumOfArtForGoodRev[rand_rev] += 1
    #                 if (NumOfArtForGoodRev[rand_rev] == z):
    #                     #del some_dict[key]
    #                      del NumOfArtForGoodRev[rand_rev]