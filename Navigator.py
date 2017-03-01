#THIS FUNCTION IS A WIP
import os
from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request, json
from flask import make_response
from Authenticator import authenticate
from DataRetriever import getProjectData, getOrganizationData, getUsers, getRepoLanguages, getCommits, getMerges, getComments, getRepositories
from Analyzer import analyzeData, trainData
from SearchController import getOrganizations, getProjects
# import mysql.connector as mariadb
# import json
# import time

# now = time.strftime("%c")
#print "Current date & time " + time.strftime("%c")


app = Flask(__name__)
authToken = 'empty token'
usersData = 'No data'

@app.route('/')
def homepage():
    if authToken == 'empty token':
        return redirect(url_for('login'))
    else:
        return render_template('homepage.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': #if submit button was pressed
        username = request.form['username'] #read username
        password = request.form['pwd']  #read password
        global authToken
        authToken = authenticate(username, password)    #call our authentication
        if(authToken == False):
            #needs an error message
            return render_template('login.html')
        else:
            #ALL THIS STUFF WILL NEED TO BE DELETED ONCE THE PROJECT STARTS CALLING FROM THE CORRECT LOCATION
            # project = input("Enter a project or organization")
            # searchResults = search('MyPureCloud', "organizations")
            # print(searchResults)
            # searchResults = search('agithub', "projects")
            # print(searchResults)
            projectName = 'allisonsteinmetz/JAM'
            #printData = getProjectData(authToken, projectName)
            # printDatas = getOrganizationData(authToken, 'railsbridge-montreal')
            #replace the redirect below with a redirect to the search page instead, when it is complete.
            return redirect(url_for('homepage'))
            #return redirect(url_for('success', data = printData))
    else: #if the user just wanted to load the page, load the page.
        return render_template('login.html')

@app.route('/search', methods=['POST'])
def search():
    searchKey = request.form['searchKey']
    searchType = request.form['searchType']
    if (searchType == "organizations"):
        results = getOrganizations(authToken, searchKey)
    else:
        results = getProjects(authToken, searchKey)
    return json.dumps(results)

@app.route('/select', methods=['POST'])
def select():
    name = request.form['name']
    print(name)
    searchType = request.form['searchType']
    if (searchType == "organizations"):
        data = getOrganizationData(authToken, name)
    else:
        data = getProjectData(authToken, name)
    # store data(pre-analyzed data) to database
    #storePreAnalysisData(name, data)
    global usersData
    usersData = analyzeData(name, data)
    # store analayzed data to database
    #storePostAnalysisData(name, userData)
    return json.dumps(usersData)

@app.route('/users')
def users():
    return render_template('usersList.html', usersData = usersData)

@app.route('/userinfo/<username>')
def showUserInfo(username):
    return render_template('user.html', name=username)

@app.route('/teaminfo/<projname>/<teamnumber>')
def showTeam(number):
    return render_template('team_information.html')
    #show the team #(number)'s stats.

@app.route('/leadershipinfo/<username>')
def showLeadership(name):
    return render_template('leadership_information.html')
    #shows a specific user's leadership info

@app.route('/contributioninfo/<username>')
def showContribution(name):
    return render_template('contribution_information.html')
    #shows a specific user's contribution info

#SUCCESS EXISTS PURELY FOR TESTING PURPOSES WHILE THE PROJECT IS IN DEVELOPMENT
@app.route('/success/<data>')
def success(data):
    return render_template('login_success.html', output=data) #calls the success.html page and feeds it the userlist as an argument

# def storePreAnalysisData(repoName, data):
#     mariadb_connection = mariadb.connect(user='root', password='l&a731', database='preAnalyzedDB')
#     cursor = mariadb_connection.cursor()
#
#     username = data.get('users')
#     language = data.get('repoLanguages')
#     commit = data.get('commits')
#     comment = data.get('comments')
#     merge = data.get('merges')
#     print(merge)
#     print(comment)
#     print(commit)
#     print(language)
#     print(username)
#     query ="DELETE FROM preData WHERE repositoryName = %s"
#     cursor.execute(query, (repoName,))
#     mariadb_connection.commit()
#     sql = "INSERT INTO preData (repositoryName, userName, currentDate, commits, comments, merges, languages) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#     cursor.execute(sql, (repoName, str(username), now, str(commit), str(comment), str(merge), str(language)))
#     mariadb_connection.commit()
#
#     return None
#
# def storePostAnalysisData(repoName, data):
#     mariadb_connection = mariadb.connect(user='root', password='l&a731', database='postAnalyzedDB')
#     cursor = mariadb_connection.cursor()
#
#     for user in data:
#         username = user.get('userLogin')
#         cont = user.get('contribution')
#         lang = user.get('languages')
#         langu = ''.join(lang)
#         team = user.get('teams')
#         teama= ''.join(team)
#         lead = user.get('leadership')
#         query ="DELETE FROM postData WHERE repositoryName = %s AND userName = %s"
#         cursor.execute(query, (repoName, username))
#         mariadb_connection.commit()
#         sql = "INSERT INTO postData (repositoryName, userName, contribution, languages, teams, leadership) VALUES (%s, %s, %s, %s, %s, %s)"
#         cursor.execute(sql, (repoName, username, cont, langu, teama, lead))
#         mariadb_connection.commit()
#     return None

def trainSystem(data):
    #contact the analyzer for training
    return None

#smariadb_connection.close()

#debug gives you information if a page fails to load.
#port number is your choice - I had to keep changing it to avoid caching (I think?) errors.
if __name__ == '__main__':
    app.run(debug=False, port = 5000)
