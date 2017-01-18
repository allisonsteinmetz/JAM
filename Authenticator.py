from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response

def authenticate(user, pwd):
    g = GitHub(user, pwd)  #use the entered username and password to authenticate
    status, data = g.issues.get() #get the status
    if(status < 400):   #if the status was not an error
        return g    #return the token
    else:   #if it was an error
        return False    #return false
