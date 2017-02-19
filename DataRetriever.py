#import pymongo

from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
#from pymongo import MongoClient

#client = MongoClient('localhost', 27017)
#db = client.test_database
#result = db.rawData.delete_many({})

token = 'nothing yet'
passed = False

def getProjectData(g, name):
    global token
    token = g
    tempList = name.split("/")
    owner = tempList[0]
    repo = tempList[1]
    userList = getUsers(owner, repo)
    repoLanguages = getRepoLanguages(owner, repo)
    commitList = getCommits(owner, repo)
    #mergeList = getMerges(user, repo)
    commentList = getComments(owner, repo)
    global passed
    passed = True
    returnData = {'users': list(userList), 'repoLanguages': repoLanguages, 'commits': commitList, 'comments':commentList}
#    projectData = {name: returnData}
#    if db.rawData.find({name:{'$exists': 1}}):
#        db.rawData.insert_one(projectData)
#    else:
#        db.rawData.replace_one({'name':name}, projectData)
#    cursor = db.rawData.find({name:{'$exists': 1}})
#    for document in cursor:
#        print(document)
    return returnData

def getOrganizationData(g, name):
    global token
    token = g
    repoList = getRepositories(name)
    for repo in repoList:
        dataPost = getProjectData(token, repo)
    return repoList

def getUsers(owner, repo):    #get a list of all the users in a project. That means collaboratros and contributors, maybe also subscribers later.
    status, data = token.repos[owner][repo].collaborators.get()
    if status == 200:
        userlist = set()
        for user in data:
            userlist.add(str(user.get('login')))
    else:
        return "-1"
    status, data = token.repos[owner][repo].contributors.get()
    if status == 200:
        for user in data:
            userlist.add(str(user.get('login')))
        return userlist
    else:
        return "-1"

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
    status, data = token.repos[owner][repo].commits.get(per_page='100')
    if status == 200:
        lastpage = 1
        commitHeader = token.getheaders()
        link = 'NULL'
        for element in commitHeader:
            if 'link' in element:
                link = element
        if link != 'NULL' :
            lastpage = link[1].split('>')[1].split('=')[3]
        commits = []
        i = 0
        while i < lastpage :
            print (i)
            status, data = token.repos[owner][repo].commits.get(per_page='100', page=i)
            codes = []
            for comm in data:
                codes.append(comm.get('sha'))
            for sha in codes:
                status, commit = token.repos[owner][repo].commits[sha].get()
                if (commit.get('committer') != None):
                    #print(commit.get('committer').get('login'))
                    #print(commit.get('commit').get('committer').get('date'))
                    #print(commit.get('commit').get('message').encode('utf-8'))
                    commitData = (commit.get('committer').get('login'), commit.get('commit').get('committer').get('date'), commit.get('commit').get('message').encode('utf-8'),
                    commit.get('stats').get('total'))
                    commits.append(commitData)
                else:
                    #print("Private User")
                    commitData = ('Private User', 'Filler_Date', 'Filler_Msg', commit.get('stats').get('total'))
                    commits.append(commitData)
            i = i + 1
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
        return "Could not retrieve comments"

def getRepositories(org):
    status, data = token.orgs[org].repos.get()
    if status == 200:
        repos = []
        for repo in data:
            repos.append(str(repo.get('full_name')))
        return repos
    else:
        return "Could not retrieve organization's repositories"
