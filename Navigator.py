#THIS FUNCTION IS A WIP
import os
from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request, json
from flask import make_response
from Authenticator import authenticate
from DataRetriever import getProjectData, getOrganizationData, getUsers, getRepoLanguages, getCommits, getMerges, getComments, getRepositories
from Analyzer import analyzeData, trainData
from SearchController import getOrganizations, getProjects
import mysql.connector as mariadb
import json
import time

now = time.strftime("%c")
#print "Current date & time " + time.strftime("%c")


app = Flask(__name__)
authToken = 'empty token'
userData = 'No data'

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
    global userData
    userData = analyzeData(data)
    # store analayzed data to database
    #storePostAnalysisData(name, userData)
    return json.dumps(userData)

@app.route('/users')
def users():
    #MAY NEED FUNCTIONALITY FOR IF SOMEONE USING THE PROGRAM CLICKS ON A USER
    return render_template('users.html', userData = userData)
    #show the user page

@app.route('/userinfo/<username>')
def showUserInfo(name):
    return render_template('user_information.html')
    #show a specific user's statis

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

def storePreAnalysisData(repoName, data):
    print repoName;
    print now;
    mariadb_connection = mariadb.connect(user='root', database='teamData')
    cursor = mariadb_connection.cursor()
    sql = "INSERT INTO team (repositoryName, currentDate, teamInfo) VALUES (%s, %s, %s)"
    cursor.execute(sql, (repoName, now, json.dumps(data)))

    mariadb_connection.commit()
    return None

def storeAnalyzedData(data):
    #store analyzed data to the correct spot in the database
    return None

def trainSystem(data):
    #contact the analyzer for training
    return None

#smariadb_connection.close()

#debug gives you information if a page fails to load.
#port number is your choice - I had to keep changing it to avoid caching (I think?) errors.
if __name__ == '__main__':
    app.run(debug=False, port = 5000)
