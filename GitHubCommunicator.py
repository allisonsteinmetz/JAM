import json
import os
from agithub.GitHub import GitHub

def gAuth(user, password):
    g = GitHub(user, password)  #use the inputted username and password to authenticate
    status, data = g.issues.get()
    if(status < 400):
        return getUsers(g)
    else:
        return status

def getUsers(g):
    status, data = g.repos.allisonsteinmetz.JAM.collaborators.get()
    if status == 200:
        userlist = []
        for user in data:
            userlist.append(str(user.get('login')))
        return userlist
    else:
        return "Could not retrieve users"

def main(): #main is basically the test case for this code
    user = raw_input('Github username: ')
    pw = raw_input('password: ')
    print (gAuth(user, pw))

main()
