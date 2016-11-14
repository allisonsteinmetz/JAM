from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
from Navigator import auth
from SearchController import openSearch

app = Flask(__name__)

pageURL = '/login'

@app.route('/login/', methods=['GET', 'POST'])
def openLogin():
    if request.method == 'POST': #if submit button was pressed
        token = validateLogin()
        if (token == False):    #if the credentials were incorrect
            return render_template('index.html')    #reload the page
            #this should display an error message instead of reloading the page
        else:   #if the credentials were correct
            userlist = getUsers(token)  #get the users
            return redirect(url_for('success', data = userlist))    #return the success page with our userlist
    else:
        return render_template('index.html')
        #currently just reloads the page, should display an error message

def loadSearch():
    return redirect(url_for('success.html', data = userlist))

def validateLogin():
    username = request.form['username'] #read username
    password = request.form['pwd']  #read password
    return auth(username, password)    #call our authentication
