import json
import os
from agithub.GitHub import GitHub

username = raw_input('Github username: ')
password = raw_input('password: ')

def main():
    g = GitHub(username, password)  #use the inputted username and password to authenticate
    status, data = g.issues.get(filter='subscribed', foobar='llama')
    output = ''.join(map(str, g.repos.allisonsteinmetz.JAM.collaborators.get()))  #turn the tuple into a string
    lookfor = "u'login'"    #this appears just before every username
    nextspot = 0    #nextspot keeps track of the current spot we're finding. We don't want to find duplicates.
    userlist = []
    while(nextspot != -1):  #nextspot returns -1 if no more names were found.
        nextspot = output.find(lookfor, nextspot+1)   #finds the lookfor phrase, starting after the current nextspot location
        if (nextspot == -1):
            break
        tempstring = output[(nextspot+12):(nextspot+52)]   #removes all the jargon before a username, and limits it to the maximum amount of username chars (+1)
        userlist.append(tempstring.partition("'")[0] )  #puts all the usernames into a list.
    #print(userlist)

main()
