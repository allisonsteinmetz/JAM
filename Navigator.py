#THIS FUNCTION IS A WIP
import json
import os
from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
from Authenticator import authenticate
from DataRetriever import getProjects, getOrganizations, getProjectData, getOrganizationData, getUsers, getRepoLanguages, getCommits, getMerges, getComments, getRepositories
from Analyzer import analyzeData, trainData


app = Flask(__name__)

@app.route('/')
def showHomepage():
    return render_template('home.html')

@app.route('/login/', methods=['GET', 'POST'])
def showLogin():
    if request.method == 'POST': #if submit button was pressed
        username = request.form['username'] #read username
        password = request.form['pwd']  #read password
        authToken = authenticate(username, password)    #call our authentication
        if(authToken == False):
            #needs an error message
            return render_template('login.html')
        else:
            #ALL THIS STUFF WILL NEED TO BE DELETED ONCE THE PROJECT STARTS CALLING FROM THE CORRECT LOCATION
            projectName = 'juicearific.Escargo'
            printData = getProjectData(authToken, projectName)
            #replace the redirect below with a redirect to the search page instead, when it is complete.
            return redirect(url_for('success', data = printData))
    else: #if the user just wanted to load the page, load the page.
        return render_template('login.html')

@app.route('/search/<searchfield>')
def showSearch():
    if request.method == 'POST': #if search button was pressed
        #Do searchy stuff here
        print("search-post placeholder")
    else: #if the page is being redirected to, display a search page with nothing in the search field yet.
        return render_template('search.html', output='')

@app.route('/projectUsers/<projname>')
def showUsers(info):
    #MAY NEED FUNCTIONALITY FOR IF SOMEONE USING THE PROGRAM CLICKS ON A USER
    return render_template('user_table.html')
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

#this will be called from the POST of showSearch - when the button is pressed it should have these arguments to pass in.
def search(criteria, type):
    if (type == "organizations"):
        results = searchOrgs(criteria)
    else:
        results = searchProjects(criteria)
    #display results
    return None

#another call from POST of showSearch - this is when a project is selected. The name and type should be known to pass as arguments.
def select(name, type):
    if (type == "organizations"):
        data = getOrgData(name)
        #store pre-analysis data to database
        analyzedData = analyzeOrg(data)
    else :
        data = getProjectData(name)
        #store pre-analysis data to database
        analyzedData = analyzeProject(data)
    #store analyzed data to database
    showUsers(analyzedData)
    return None

def storePreAnalysisData(data):
    #store data to correct spot in database
    return None

def storeAnalyzedData(data):
    #store analyzed data to the correct spot in the database
    return None

def trainSystem(data):
    #contact the analyzer for training
    return None

#debug gives you information if a page fails to load.
#port number is your choice - I had to keep changing it to avoid caching (I think?) errors.
if __name__ == '__main__':
    app.run(debug=False, port = 4979)
