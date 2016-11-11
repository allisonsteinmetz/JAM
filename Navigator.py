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
