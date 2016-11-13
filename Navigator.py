#THIS FUNCTION IS A WIP
from GitHubCommunicator import authenticate
from DataRetriever import retrieveProjs, retrieveOrgs, retrieveUsers, retrieveMerges, retrieveCommits, retrieveLanguages, retrieveCommits, retrieveRepositories

@app.route('/')
def homepage():
    return render_template('home.html')

def auth(user, pw):
    token = authenticate(user, pw)
    if(token == False):
        #return error message
    else:
        #display search page

def showSearch():
    #show search page

def search(criteria, type):
    if (type == "organizations"):
        results = searchOrgs(criteria)
    else:
        results = searchProjects(criteria)
    #display results

def select(name, type):
    if (type == "organizations"):
        data = getOrgData(name)
        analyzedData = analyzeOrg(data)
    else :
        data = getProjectData(name)
        analyzedData = analyzeProject(data)
    #store results to database
    showUsers(analyzedData)

def showUsers(info):
    #show the user page

def showUserInfo(name):
    #show a specific user's statis

def showTeam(number):
    #show the team #(number)'s stats.

def showLeadership(name):
    #shows a specific user's leadership info

def showContribution(name):
    #shows a specific user's contribution info
