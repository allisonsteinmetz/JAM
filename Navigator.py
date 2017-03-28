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
name = 'No Project Name'

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
            return redirect(url_for('homepage'))
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
    global name
    name = request.form['name']
    print(name)
    searchType = request.form['searchType']
    if (searchType == "organizations"):
        data = getOrganizationData(authToken, name)
    else:
        data = getProjectData(authToken, name)

    global usersData
    usersData = analyzeData(name, data)
    return json.dumps(usersData)

@app.route('/users')
def users():
    print(usersData)
    return render_template('usersList.html', projectName = name,usersData = usersData)

@app.route('/userinfo/<username>/<index>')
def showUserInfo(username, index):
    return render_template('user.html', name=username, userData = usersData[int(index) - 1])

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

def trainSystem(data):
    #contact the analyzer for training
    return None

#smariadb_connection.close()

#debug gives you information if a page fails to load.
#port number is your choice - I had to keep changing it to avoid caching (I think?) errors.
if __name__ == '__main__':
    app.run(debug=False, port = 5000)
