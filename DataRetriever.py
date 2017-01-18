import pymongo

from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test_database
token = 'nothing yet'

def getProjectData(g, name):
    global token
    token = g
    tempList = name.split(".")
    owner = tempList[0]
    repo = tempList[1]
    userList = getUsers(owner, repo)
    repoLanguages = getRepoLanguages(owner, repo)
    commitList = getCommits(owner, repo)
    #mergeList = getMerges(user, repo)
    commentList = getComments(owner, repo)
    returnData = {'repoLanguages': repoLanguages, 'commits': commitList, 'comments':commentList}
    db.rawData.insert_one(returnData)
    # cursor = db.rawData.find()
    # for document in cursor:
    #     print(document)
    returnData = userList
    return returnData

def getOrganizationData(g, name):
    global token
    token = g
    repoList = getRepositories(name)
    #for each repo, do the things we do in "getProjectData". Then combine all the data together for analysis.
    return None

def getUsers(owner, repo):    #get a list of all the users in a project. That means collaboratros and contributors, maybe also subscribers later.
    status, data = token.repos[owner][repo].collaborators.get()
    if status == 200:
        userlist = set()
        for user in data:
            userlist.add(str(user.get('login')))
    else:
        return "Could not retrieve collaborators"
    status, data = token.repos[owner][repo].contributors.get()
    if status == 200:
        for user in data:
            userlist.add(str(user.get('login')))
        return userlist
    else:
        return "Could not retrieve contributors"

def getRepoLanguages(owner, repo):
    status, data = token.repos[owner][repo].languages.get()
    if status == 200:
        languages = []
        for language in data:
            languages.append(str(language))
        return languages
    else:
        return "Could not retrieve languages"

def getCommits(owner, repo):
    status, data = token.repos[owner][repo].commits.get()
    if status == 200:
        commits = []
        for commit in data:
            commits.append(commit.get('commit'))
        return commits
    else:
        return "Could not retrieve commits"

def getMerges(owner, repo):
    print('work in progress')
    return None

def getComments(owner, repo):
    status, data = token.repos[owner][repo].comments.get()
    if status == 200:
        comments = []
        for comment in data:
            comments.append(comment)
        return comments
    else:
        return "Could not retrieve languages"

def getRepositories(org):
    print ('work in progress')
    return None
