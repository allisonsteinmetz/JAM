from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
import mysql.connector as mariadb
import json
import time

now = time.strftime("%c")

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
    returnData = {'users': list(userList), 'repoLanguages': repoLanguages, 'commits': commitList, 'comments':commentList, 'merge': 'WIP'}
    storePreAnalysisData(name, returnData)
    return returnData

def getOrganizationData(g, name):
    global token
    token = g
    repoList = getRepositories(name)
    returnData = []
    for repo in repoList:
        dataPost = getProjectData(token, repo)
        returnData.append(dataPost)
    # do we want to store organization data differently???
    storePreAnalysisData(name, returnData)
    return repoList

def getUsers(owner, repo):    #get a list of all the users in a project. That means collaboratros and contributors, maybe also subscribers later.
    strikeone = False
    status, data = token.repos[owner][repo].collaborators.get()
    userlist = set()
    if status == 200:
        for user in data:
            userlist.add(str(user.get('login')))
    else:
        strikeone = True
    status, data = token.repos[owner][repo].contributors.get()
    if status == 200:
        for user in data:
            userlist.add(str(user.get('login')))
        return userlist
    elif strikeone :
        return -1
    else:
        return userlist

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
    branches = []   #create a location to store all branches
    status, data = token.repos[owner][repo].branches.get(per_page=100)  #grab list of all branches
    if status == 200 :    #check to see if the data pulled successfully
        #determine if there are more than one page of results
        lastpage = '1'
        branchHeader = token.getheaders()
        link = 'NULL'
        for element in branchHeader:
            if 'link' in element:
                link = element
        #if there is more than one page of results:
        if link != 'NULL' :
            lastpage = link[1].split('>')[1].split('=')[3]  #grab the last page num
            i = 0
            for branch in data :
                branches.append(branch.get('name')) #append the first page into the array
            while i < int(lastpage) :
                status, data = token.repos[owner][repo].branches.get(per_page='100', page=i)
                if status == 200 :
                    for branch in data :
                        branches.append(branch.get('name')) #append the branches from each page into the array
        #for every branch in the repository:
        for branch in data:
            branchName = branch.get('name')
            print(branchName)
            status, data = token.repos[owner][repo].commits.get(sha=branchName, per_page=100)   #grab all the commits.
            if status == 200:
                lastpage = '1'
                commitHeader = token.getheaders()
                link = 'NULL'
                for element in commitHeader:
                    if 'link' in element:
                        link = element
                if link != 'NULL' :
                    lastpage = link[1].split('>')[1].split('=')[4]
                commits = []
                i = 1
                while i <= int(lastpage) :
                    print (i)
                    status, data = token.repos[owner][repo].commits.get(sha=branchName, per_page='100', page=i)
                    codes = []
                    for comm in data:
                        codes.append(comm.get('sha'))
                    for sha in codes:
                        status, commit = token.repos[owner][repo].commits[sha].get()
                        if (commit.get('committer') != None):
                            #print(commit.get('committer').get('login'))
                            #print(commit.get('commit').get('committer').get('date'))
                            #print(commit.get('commit').get('message').encode('utf-8'))
                            filenames = []
                            for f in commit.get('files') :
                                filenames.append(f.get('filename'))
                            commitData = (commit.get('committer').get('login'), commit.get('commit').get('committer').get('date'), commit.get('commit').get('message').encode('utf-8'),
                                commit.get('stats').get('total'), branchName, filenames)
                            #print(commit.get('commit').get('committer').get('date'))
                            #print(commitData)
    #dict[0] = username; dict[1] = commit date; dict[2] = message w/ commit; dict[3] = total lines of code changed;
    #dict[4] = branch name; dict[5] = list of files changed
                        #print(commitData)
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

def storePreAnalysisData(repoName, data):
    mariadb_connection = mariadb.connect(user='root', password='l&a731', database='preAnalyzedDB')
    cursor = mariadb_connection.cursor()

    username = data.get('users')
    language = data.get('repoLanguages')
    commit = data.get('commits')
    comment = data.get('comments')
    merge = data.get('merges')
    # print(merge)
    # print(comment)
    # print(commit)
    # print(language)
    # print(username)
    query ="DELETE FROM preData WHERE repositoryName = %s"
    cursor.execute(query, (repoName,))
    mariadb_connection.commit()
    sql = "INSERT INTO preData (repositoryName, userName, currentDate, commits, comments, merges, languages) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (repoName, str(username), now, str(commit), str(comment), str(merge), str(language)))
    mariadb_connection.commit()

    return None
