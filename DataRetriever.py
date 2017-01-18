from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response

token = 'nothing yet'

def getProjects(g):
    #this is for the search page
    #find relevant projects, return them.
    return None

def getProjectData(g, name):
    global token
    token = g
    tempList = name.split(".")
    user = tempList[0]
    repo = tempList[1]
    userList = getUsers(user, repo)
    repoLanguages = getRepoLanguages(user, repo)
    commitList = getCommits(user, repo)
    #mergeList = getMerges(user, repo)
    commentList = getComments(user, repo)
    #returnData = {'users': userList, 'repoLanguages': repoLanguages, 'commits': commitList, 'comments':commentList}
    returnData = userList
    #combine all the data and return it
    return returnData

def getOrganizations(g):
    #this is for the search page
    #find relevant orgs, return them.
    return None

def getOrganizationData(g, name):
    global token
    token = g
    repoList = getRepositories(name)
    #for each repo, do the things we do in "getProjectData". Then combine all the data together for analysis.
    return None

def getUsers(login, repo):    #get a list of all the users in a project. That means collaboratros and contributors, maybe also subscribers later.
    status, data = token.repos[login][repo].collaborators.get()
    if status == 200:
        userlist = set()
        for user in data:
            userlist.add(str(user.get('login')))
    else:
        return "Could not retrieve collaborators"
    status, data = token.repos[login][repo].contributors.get()
    if status == 200:
        for user in data:
            userlist.add(str(user.get('login')))
        return userlist
    else:
        return "Could not retrieve contributors"

def getRepoLanguages(login, repo):
    status, data = token.repos[login][repo].languages.get()
    if status == 200:
        languages = []
        for language in data:
            languages.append(str(language))
        return languages
    else:
        return "Could not retrieve languages"

def getCommits(login, repo):
    status, data = token.repos[login][repo].commits.get()
    if status == 200:
        commits = []
        for commit in data:
            commits.append(commit.get('commit'))
        return commits
    else:
        return "Could not retrieve commits"

def getMerges(login, repo):
    print('work in progress')
    return None

def getComments(login, repo):
    status, data = token.repos[login][repo].comments.get()
    if status == 200:
        print(data)
        comments = []
        for comment in data:
            comments.append(comment)
        return comments
    else:
        return "Could not retrieve languages"

def getRepositories(org):
    print ('work in progress')
    return None
