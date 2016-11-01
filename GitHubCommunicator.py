import json
import os
from agithub.GitHub import GitHub

def G_Auth(UN, PW):
    g = GitHub(UN, PW)  #use the inputted username and password to authenticate
    status, data = g.issues.get(filter='subscribed', foobar='llama')
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
        return "Could not retireve users"

def main(): #main is basically the test case for this code
    user = raw_input('Github username: ')
    pw = raw_input('password: ')
    print (G_Auth(user, pw))

main()
