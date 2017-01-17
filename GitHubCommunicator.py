import json
import os
from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
#from flask.ext.mysql import MySQL

app = Flask(__name__)
# mysql = MySQL()
#
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'german2013'
# app.config['MYSQL_DATABASE_DB'] = 'Proj_Test'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
#
# conn = mysql.connect()
# cursor = conn.cursor()


#Authenticates a user based on username and password.
#invalid credentials currently reloads the page.
@app.route('/authenticate/')
def authenticate(user, pwd):
    g = GitHub(user, pwd)  #use the entered username and password to authenticate
    status, data = g.issues.get() #get the status
    if(status < 400):   #if the status was not an error
        return g    #return the token
    else:   #if it was an error
        return False    #return false

#prints out the data on a success page
@app.route('/success/<data>')
def success(data):
    return render_template('success.html', output=data) #calls the success.html page and feeds it the userlist as an argument

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': #if submit button was pressed
        username = request.form['username'] #read username
        password = request.form['pwd']  #read password

        args = 'Proj_Test3'
        # cursor.callproc('store_proj_v2', ([args,]))
        # cursor.execute ("SELECT proj_id, test_data FROM Project")
        # conn.commit()
        # data = cursor.fetchall()
        # for row in data :
        #     print row[0], row[1]


        token = authenticate(username, password)    #call our authentication
        if (token == False):    #if the credentials were incorrect
            return render_template('index.html')    #reload the page
        else:   #if the credentials were correct
            userlist = getUsers(token)  #get the users
            languages = getLanguages(token) # get languages used in repo
            return redirect(url_for('success', data = userlist))    #return the success page with our userlist
    else:
        return render_template('index.html')

#gets a list of users from our predefined project.
def getUsers(g):
    status, data = g.repos.allisonsteinmetz.JAM.collaborators.get()
    if status == 200:
        userlist = set()
        for user in data:
            userlist.add(str(user.get('login')))
    else:
        return "Could not retrieve collaborators"
    status, data = g.repos.allisonsteinmetz.JAM.contributors.get()
    if status == 200:
        for user in data:
            userlist.add(str(user.get('login')))
        return userlist
    else:
        return "Could not retrieve contributors"

def getLanguages(g):
    status, data = g.repos.allisonsteinmetz.JAM.languages.get()
    if status == 200:
        languages = []
        print(data)
        for language in data:
            print(language)
            #languages.append(language)
    else:
        return "Could not retrieve languages"

#just a homepage I was using for testing
@app.route('/')
def hello():
    return 'Test Homepage'

#debug gives you information if a page fails to load.
#port number is your choice - I had to keep changing it to avoid caching (I think?) errors.
if __name__ == '__main__':
    app.run(debug=False, port = 4972)
