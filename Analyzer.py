#IF THIS CODE DOESN'T WORK RIGHT NOW:
#comment out the "import matplotlib.pyplot as plt"
#comment out the calling of calcTeams
#should then work again

from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
import mysql.connector as mariadb
import numpy as np
from sklearn.cluster import MeanShift
#import matplotlib.pyplot as plt
import json
import time

now = time.strftime("%c")

default = 0
contDict = {}
commitCount = {}
userLangs = {}
statsDict = {}
branchList = []
fileList = []
dateList = []
fileExtensions = []
fileVals = {}
dateVals = {}
branchVals = {}

global users
def analyzeData(name, data):
    userStats = []
    global users
    users = data.get('users')
    calcContribution(data)
    assignVals(data)
    calcTeams(data)
    for user in users:
        tempDict = {'userLogin': user, 'contribution': contDict.get(user), 'languages': userLangs.get(user),
            'teams': 'WIP', 'leadership': 'WIP', 'uniqueStats' : statsDict.get(user)}
        userStats.append(tempDict)
    storePostAnalysisData(name, userStats)
    tempDict = {'userLogin': '-', 'contribution': contDict.get('-'), 'languages': '', 'teams': 'WIP', 'leadership': 'WIP', 'uniqueStats' :statsDict.get('-')}
    userStats.append(tempDict)
    return userStats
#    commitList = data.get('commits')
#    arglist = []
#    for i in commitList:
#        arglist.append(i[2].encode('utf-8'))
#    searchWords(arglist)
def calcTeams(data):
    commits = data.get('commits')
    analyzeThis = []
    for comm in commits:
        branchvalue = branchVals[comm[4]]
        filevalue = 0
        filecount = 0
        for f in comm[5]:
            filevalue += fileVals[f]
            filecount += 1
        filevalue = float(filevalue) / filecount
        datevalue = dateVals[comm[1].split('T')[0]]
        commData = [branchvalue, filevalue, datevalue]
        analyzeThis.append(commData)

    ms = MeanShift()
    ms.fit(analyzeThis)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    n_clusters_ = len(np.unique(labels))
    print("Number of estimated clusters:", n_clusters_)
    colors = 10*['r.','g.','b.','c.','k.','y.','m.']

    for i in range(len(analyzeThis)):
        plt.plot(analyzeThis[i][0], analyzeThis[i][2], colors[labels[i]], markersize = 10)

    plt.scatter(cluster_centers[:,0], cluster_centers[:,1],
        marker = "x", s=150, linewidths = 5, zorder=10)

    for c in cluster_centers:
        print(c)

    #plt.show()

def assignVals(data):
    branchCount = 0
    for b in branchList:
        branchVals[b] = branchCount
        branchCount += 5
    extVals = {}
    feCount = 0
    for fe in fileExtensions:
        extVals[fe] = feCount
        feCount += 5
    for f in fileList:
        e = f.split('.')
        ext = e[len(e)-1]
        fileVals[f] = extVals[ext]
        extVals[ext] += .05
    commits = data.get('commits')
    start = commits[len(commits)-1][1]
    startDate_unformatted = start.split('T')[0]
    startDate = convertDate(startDate_unformatted)
    for d in dateList:
        date = convertDate(d)
        score = ((date[1] - startDate[1]) * 365) + (date[0] - startDate[0])
        score = float(score) / 100
        dateVals[d] = score
    #print(branchVals)
    #print(fileVals)
    #print(dateVals)

def convertDate(date):
    formatted = date.split('-')
    months = {'01': 0, '02': 31, '03': 59, '04': 90, '05': 120, '06': 151, '07': 181, '08': 212, '09': 243, '10': 273, '11': 304, '12':334}

    fdate = [months[formatted[1]] + int(formatted[2]), int(formatted[0])]
    return fdate

def calcContribution(data):
    total_score = 0
    total_commits = 0
    total_codeLines = 0
    commits = data.get('commits')
    comments = data.get('comments')
    #print(users)
    for user in users:
        #print(user)
        contDict[user] = 0
        userLangs[user] = []
        branches = {}
        bCount = []
        statsDict[user] = {'commitCount' : 0, 'codeLines' : 0, 'acceptedCommits' : 0, 'acceptedLines' : 0, 'commentCount' : 0, 'branches' : branches}
    statsDict['-'] = {'commitCount' : 0, 'codeLines' : 0, 'acceptedCommits' : 0, 'acceptedLines' : 0, 'commentCount' : 0, 'branches' : branches}
    for comm in commits:
        if comm[4] not in branchList:
            branchList.append(comm[4])
        for f in comm[5]:
            if f not in fileList:
                fileList.append(f)
                ext = f.split('.')
                if ext[len(ext) - 1] not in fileExtensions:
                    fileExtensions.append(ext[len(ext)-1])
        if comm[1].split('T')[0] not in dateList:
            dateList.append(comm[1].split('T')[0])
        userLogin = comm[0]
        if (userLogin != 'Private User') and (userLogin != 'web-flow'):
            filenames = comm[5]
            if comm[3] > 9:
                for f in filenames:
                    #print(f)
                    extension = f.split('.')
                    last = len(extension) - 1
                    if extension[last] == 'py':
                        if 'Python' not in userLangs[userLogin]:
                            userLangs[userLogin].append('Python')
                    elif extension[last] == 'js':
                        if 'JavaScript' not in userLangs[userLogin]:
                            userLangs[userLogin].append('JavaScript')
                    elif extension[last] == 'html':
                        if 'HTML' not in userLangs[userLogin]:
                            userLangs[userLogin].append('HTML')
            #print(userLogin)
            score = (comm[3] / float(6))
            total_score += score
            existingScore = contDict.setdefault(userLogin, 0)
            contDict[userLogin] = existingScore + score
            statsDict[userLogin]['commitCount'] += 1
            total_commits += 1
            statsDict[userLogin]['codeLines'] += comm[3]
            total_codeLines += comm[3]
            if comm[4] not in statsDict[userLogin]['branches']:
                statsDict[userLogin]['branches'].update({comm[4] : comm[3]})
            else :
                statsDict[userLogin]['branches'][comm[4]] += comm[3]
            non_private_total_score = total_score
    #print('hit it')
    for user in users:
        temp = contDict[user]
        cont_decimal = temp/float(non_private_total_score)
        cont_percent = "{:.2f}".format(cont_decimal * 100)
        #print(user)
        #print(cont_percent)
        contDict[user] = cont_percent
    statsDict['-']['commitCount'] = total_commits
    statsDict['-']['codeLines'] = total_codeLines
    contDict['-'] = total_score
    return 1;
    #Create dictionary
    #add each user and a list of ints (per) to the dictionary
    #go through all commits, add to the appropriate list
    #print(commits)
    #print(users)

def searchWords(data):
    #this is what will end up using scikit
    #vocabulary = "tests python javascript html test testing repositories".split()
    #vect = TfidfVectorizer(sublinear_tf=True, max_df=0.5, analyzer='word',
    #       stop_words='english', vocabulary=vocabulary, input='content')
    #analyzedData = vect.fit_transform(data).toarray()
    #print(analyzedData)

    vocab = ['alli', 'github', 'josh', 'flask', 'the']
    vectorizer = CountVectorizer(min_df=1, vocabulary = vocab)
    x = vectorizer.fit_transform(data)
    analyzedData = x.toarray()
    print(analyzedData)
    print(vectorizer.get_feature_names())
    return analyzedData

def trainData(data):
    #this is going to be training the system
    #load in a file named after a programming language
    #file will be formatted as such:
    #alli pointed out we may be able to look at the file name. I will be looking into this soon.
    #GUARANTEED:
    #word, word, word...
    #etc.
    #ACCEPTED:
    #word, word, word, word, word, word...
    #word, word, word, word, word, word...
    #etc.
    #UNACCEPTED:
    #word, word...
    #etc.
    #accepted words make the code think it was that programming language. unacceppted words automatically
    #throw out the language as an option (meaning either they aren't programming in it, or they do not know
    #the language well enough to know that it doesn't exist in that language)
    if worked:
        return true
    else:
        return false

def storePostAnalysisData(repoName, data):
    mariadb_connection = mariadb.connect(user='masterjam', password='jamfordays',host='myrd.csducou8syzm.us-east-1.rds.amazonaws.com', database='postAnalyzedDB')
    cursor = mariadb_connection.cursor()

    for user in data:
        username = user.get('userLogin')
        cont = user.get('contribution')
        lang = user.get('languages')
        langu = ''.join(lang)
        team = user.get('teams')
        teama= ''.join(team)
        lead = user.get('leadership')
        query ="DELETE FROM postData WHERE repositoryName = %s AND userName = %s"
        cursor.execute(query, (repoName, username))
        mariadb_connection.commit()
        sql = "INSERT INTO postData (repositoryName, userName, contribution, languages, teams, leadership) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (repoName, username, cont, langu, teama, lead))
        mariadb_connection.commit()
    return None
