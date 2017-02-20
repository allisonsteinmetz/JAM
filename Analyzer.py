from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

default = 0
contDict = {}

def analyzeData(data):
    contData = calcContribution(data)
#    commitList = data.get('commits')
#    arglist = []
#    for i in commitList:
#        arglist.append(i[2].encode('utf-8'))
#    searchWords(arglist)

def calcContribution(data):
    commits = data.get('commits')
    users = data.get('users')
    comments = data.get('comments')
    if(users == "-1"):
        print("We could not complete user list")
        return;
    for user in users:
        #print(user)
        contDict[user] = 0
    contDict['Private User'] = 0
    for comm in commits:
        userLogin = comm[0]
        #print(userLogin)
        score = (comm[3] / 6)
        existingScore = contDict.setdefault(userLogin, 0)
        contDict[userLogin] = existingScore + score
    #for user in contDict:
        #print(user)
        #print(str(contDict.get(user)))
        #print(" ")
    return True;
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
