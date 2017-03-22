# lines of code accepted
# commits accepted
# major contribution branches
# # of comments

from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
#from sklearn.feature_extraction import DictVectorizer
#from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import mysql.connector as mariadb
import json
import time

now = time.strftime("%c")

default = 0
contDict = {}
commitCount = {}
userLangs = {}
statsDict = {}
global users
def analyzeData(name, data):
    userStats = []
    global users
    users = data.get('users')
    calcContribution(data)
    for user in users:
        tempDict = {'userLogin': user, 'contribution': contDict.get(user), 'languages': userLangs.get(user),
            'teams': 'WIP', 'leadership': 'WIP', 'uniqueStats' : statsDict.get(user)}
        userStats.append(tempDict)
    storePostAnalysisData(name, userStats)
    return userStats
#    commitList = data.get('commits')
#    arglist = []
#    for i in commitList:
#        arglist.append(i[2].encode('utf-8'))
#    searchWords(arglist)

def calcContribution(data):
    total_score = 0
    commits = data.get('commits')
    comments = data.get('comments')
    #print(users)
    for user in users:
        #print(user)
        contDict[user] = 0
        userLangs[user] = []
        branches = []
        statsDict[user] = {'commitCount' : 0, 'codeLines' : 0, 'acceptedCommits' : 0, 'acceptedLines' : 0, 'commentCount' : 0, 'branches' : branches}
    #contDict['Private User'] = 0
    #statsDict['Private User'] =

    #contDict['web-flow'] = 0
    #commitCount['web-flow'] = 0
    for comm in commits:
        #print(comm)
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
            statsDict[userLogin]['codeLines'] += comm[3]
            non_private_total_score = total_score
    #print('hit it')
    for user in users:
        temp = contDict[user]
        cont_percent = temp/float(non_private_total_score)
        #print(user)
        #print(cont_percent)
        contDict[user] = cont_percent
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
    mariadb_connection = mariadb.connect(user='root', password='l&a731', database='postAnalyzedDB')
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
