import json
import os
from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for, redirect, request
from flask import make_response

app = Flask(__name__)

def gAuth(user, password):
    g = GitHub(user, password)  #use the entered username and password to authenticate
    status, data = g.issues.get()
    if(status < 400):
        return g
    else:
        return false

def getUsers(g):
    status, data = g.repos.allisonsteinmetz.JAM.collaborators.get()
    if status == 200:
        userlist = []
        for user in data:
            userlist.append(str(user.get('login')))
        return userlist
    else:
        return "Could not retrieve users"

@app.route('/authenticate/<user>/<pw>')
def main(user, pw): #main is basically the test case for this code
    #request = json.load(sys.stdin)
    #response = handle_request(request)
    #print (json.dump(response, sys.stdout, indent=2))

    # user = raw_input('Github username: ')
    # pw = raw_input('password: ')
    print("started")
    g = gAuth(user, pw)
    if (g):
        userList = getUsers(g)
        json_userList = json.dumps(userList)
        print(json.dumps(json_userList, indent=2))
        return json_userList

if __name__ == '__main__':
    app.run()
