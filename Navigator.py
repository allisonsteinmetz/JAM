#THIS FUNCTION IS A WIP
import os
from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request, json
from flask import make_response
from Authenticator import authenticate
from DataRetriever import getProjectData, getOrganizationData, getUsers, getRepoLanguages, getCommits, getMerges, getComments, getRepositories
from Analyzer import analyzeData
from SearchController import getOrganizations, getProjects
import mysql.connector as mariadb
import json
from datetime import datetime
from dateutil.parser import parse as parse_date



app = Flask(__name__)
authToken = 'empty token'
usersData = 'No data'
projName = 'No Project Name'
totalData = 'None'

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
    global projName
    projName = request.form['name']
    print(projName)
    searchType = request.form['searchType']
    # if postanalyzed data retrieved long than an hour ago

    mariadb_connection = mariadb.connect(user='masterjam', password='jamfordays',host='myrd.csducou8syzm.us-east-1.rds.amazonaws.com', database='preAnalyzedDB')
    cursor = mariadb_connection.cursor()
    cursor = mariadb_connection.cursor(buffered=True)
    query = "SELECT currentDate FROM preData WHERE repositoryName = %s ORDER BY currentDate ASC LIMIT 1"
    cursor.execute(query, (projName,))
    mariadb_connection.commit()
    result = cursor.fetchone()
    # f = '%Y-%m-%d %H:%M:%S,'
    #
    # present = time.now()
    # retrievedDate = datetime.strptime(str(result), f)
    # presentDate = datetime.strptime(present, f)
    #
    # print(retrievedDate)

    present = datetime.now()
    retrievedDate = result[0]

    unicode_text = retrievedDate
    dt = parse_date(unicode_text)

    print(dt) #analyzed date and time
    print(present) #present date and time

    timeDiff = present - dt
    if (timeDiff.seconds <= 3600):
        print("project was analyzed less than an hour ago")

    else
        print("project was analyzed longer than an hour ago")







    if (searchType == "organizations"):
        print(datetime.now())
        data = getOrganizationData(authToken, projName)
    else:
        print(datetime.now())
        data = getProjectData(authToken, projName)

    global usersData
    usersData = analyzeData(projName, data)

    # else pull analyzeData from database and continue

    global totalData
    totalData = usersData[len(usersData) - 1]
    print totalData
    print(datetime.now())
    return json.dumps(usersData)

@app.route('/users')
def users():
    print(usersData)
    return render_template('usersList.html', projectName = projName, usersData = usersData)

@app.route('/userinfo/<username>/<index>')
def showUserInfo(username, index):
    return render_template('user.html', projectName = projName, userData = usersData[int(index) - 1], totalData = totalData, data = usersData)

def trainSystem(data):
    #contact the analyzer for training
    return None

#debug gives you information if a page fails to load.
#port number is your choice - I had to keep changing it to avoid caching (I think?) errors.
if __name__ == '__main__':
    app.run(debug=False, port = 5000)
