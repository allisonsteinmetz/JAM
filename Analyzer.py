from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
import mysql.connector as mariadb
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
import json
from datetime import datetime

present = datetime.now()

default = 0
contDict = {}       #holds the contribution score of each user, as calculated in calcContribution.
commitCount = {}    #holds the number of commits each user has made, for use in calcContribution.
userLangs = {}      #holds the languages each user has coded in, for use in calcContribution.
statsDict = {}      #holds the statistics about each user. These are generally found in calcContribution.
branchList = []     #holds a list of all branches, for use in multiple parts of the analyzer.
fileList = []       #holds a list of all the files with valid extensions. For use in calcTeams.
dateList = []       #holds a list of all dates that commits were made on. For use in assignVals.
userTeamList = []   #holds a list of all users to be considered as on teams.
global fileExtensions #holds a list of all valid file extensions. Pulled from the database. For use in calcTeams.
fileVals = []       #holds a list of all files which we will be using binary values for. For use in calcTeams.
startDate = []      #holds the date that the first commit was made on. For use in assignVals.
dateVals = {}       #holds a list of values for all the dates that commits were made on. For use in calcTeams.
branchVals = {}     #holds a list of values for branches. Branch values are enough to guarantee different clusters. used in calcTeams.
userTeams = {}      #holds a dictionary of lists (one entry per user), containing the information for which teammates each user has.
fileLeaders = {}    #holds a dictionary which contains an entry for each valid file (held in fileList), with each entry holding a dictionary, an entry for each user.
branchLeaders = {}  #same format as fileLeaders, except for branches instead of files.
userLeadership = {} #holds a score for each user related to their leadership abilities.
global users        #will hold a list of all users.

def analyzeData(name, data):
    userStats = []  #holds the array of all data we will return.
    global users                #modify the global users variable, don't create a local one.
    users = data.get('users')   #get a list of all users from our pull.
    makeLists(data)             #make a list of all branches, files, and dates that commits were made on.
    calcContribution(data)      #calculate contribution for each user.
    determineValidTeamUsers()   #determine which users have contributed enough to be considered for teams
    assignVals(data)            #assign values to branches and dates for use in clustering.
    calcTeams(data)             #calculate which user work with what other users.
    calcLeadership()            #calculate which users led the most by way of branches and files led (most commits to them)
    for user in users:          #for each user, package the data in a way that can be easily parsed on return.
        tempDict = {'userLogin': user, 'contribution': contDict.get(user), 'languages': userLangs.get(user),
            'teams': userTeams.get(user), 'leadership': userLeadership.get(user), 'uniqueStats' : statsDict.get(user)}
        userStats.append(tempDict)  #and add that data to the return data.
    storePostAnalysisData(name, userStats)     #store the data to the database in a post-analyzed form.
    tempDict = {'userLogin': '-', 'contribution': contDict.get('-'), 'languages': '', 'teams': userTeams.get('-'), 'leadership': '10.00', 'uniqueStats' :statsDict.get('-')}
    userStats.append(tempDict)  #store a "total" user. Name '-' cannot be used in GitHub.
    return userStats    #return the data.

def determineValidTeamUsers():
    userCount = float(len(contDict) - 1)    #a count of all users on the project. -1 is to remove the total user.
    threshhold = (100 / userCount) / 3      #calculate a threshhold, of equal split divided by 3 (a third of equal responsibility)
    for c in contDict:          #for each user:
        if c is '-':            #skip if it's the total User
            continue
        contValue = float(contDict[c])  #otherwise grab their value (and convert from string to float)
        if contValue >= threshhold:     #if they contriuted more than the threshhold
            userTeamList.append(c)      #add them to the list we will find team members for.
    return

def makeLists(data):
    #call the database get function here instead
    global fileExtensions
    fileExtensions = {'py' : 'Python', 'java' : 'Java', 'class' : 'C#', 'cpp' : 'C++', 'cxx' : 'C++', 'js' : 'JavaScript', 'html' : 'HTML'}
    #end call the database get function here instead
    commits = data.get('commits')       #grab all the commits
    for comm in commits:                #for each one, check:
        if comm[4] not in branchList:   #for new branches, not already in the list
            branchList.append(comm[4])
        for f in comm[5]:               #for new files, not already in the list
            if f not in fileList:
                fileList.append(f)
                ext = f.split('.')
        tempdate = comm[1].split('T')[0]
        if tempdate not in dateList:    #for new dates, not already in the list.
            dateList.append(tempdate)
    #determine which files we will be evaluating.
    extList = []    #make a new list for all valid file extensions
    for fe in fileExtensions:   #find all valid extensions
        extList.append(fe)   #put them in the list
    for f in fileList:          #for every file we've found:
        e = f.split('.')        #find its extension.
        ext = e[len(e)-1]
        if ext in extList:      #if that extension is in thelist
            fileVals.append(f)  #add the file to the list of files we will evaluate.

    start = commits[len(commits)-1][1]  #Format the date of the first commit
    startDate_unformatted = start.split('T')[0]
    startDate_formatted = convertDate(startDate_unformatted)
    startDate.append(startDate_formatted[0])
    startDate.append(startDate_formatted[1])    #store it into the global variable
    for f in fileVals:
        fileLeaders[f] = {}
        for user in users:
            fileLeaders[f][user] = 0
    for b in branchList:
        branchLeaders[b] = {}
        for user in users:
            branchLeaders[b][user] = 0
    for user in users:
        userLeadership[user] = 0
    return

def calcLeadership():
    for b in branchLeaders:     #for each branch:
        currentuserval = 0      #set a default, max value and name
        currentusername = 'none'
        for user in branchLeaders[b]:   #compare that to each user:
            nextuserval = branchLeaders[b][user]
            if nextuserval > currentuserval:    #if the user we're comparing to is higher:
                currentuserval = nextuserval    #change the max to be them.
                currentusername = user
            elif nextuserval == currentuserval: #if they tie:
                temp = '-' + currentusername + '.' + user   #add them to the list of leaders.
                currentusername = temp
        if b == 'master':   #assign branch score values. Master is worth more as it is generally more important.
            score = 5
        else:
            score = 3
        if currentusername[0] is '-':   #if there are multiple leaders on a branch:
            names = currentusername.split('.')  #split them into readable names
            names[0] = names[0][1:]
            for n in names:
                userLeadership[n] += (score / float(len(names)))   #assign an adjusted score based on sharing
                statsDict[n]['branchesLed'] += 1            #keep track of this for unique statistics
        else:
            userLeadership[currentusername] += score    #otherwise just assign the regular score.
    for f in fileLeaders:   #for each file:
        currentuserval = 0  #set a default, max value and name
        currentusername = 'none'
        for user in fileLeaders[f]:     #compare that to each user:
            nextuserval = fileLeaders[f][user]
            if nextuserval > currentuserval:    #if the user we're comparing to is higher:
                currentuserval = nextuserval    #change the max to be them.
                currentusername = user
            elif nextuserval == currentuserval: #if they tie:
                temp = '-' + currentusername + '.' + user   #add them to the list of leaders.
                currentusername = temp
        if currentusername[0] is '-':   #if there are multiple leaders on the file:
            names = currentusername.split('.')  #split them into readable names
            names[0] = names[0][1:]
            if names[0] is 'none':
                names.remove('none')
            for n in names:
                userLeadership[n] += (1 / float(len(names)))   #assign an adjusted score based on sharing
                statsDict[n]['filesLed'] += 1       #keep track of this for unique statistics
        else:
            userLeadership[currentusername] += 1    #otherwise just assign 1

    max_leader = 0      #set a variable to keep track of the max points
    for user in userLeadership: #check each user's points
        if userLeadership[user] > max_leader:
            max_leader = userLeadership[user]   #set a new max if they're better

    for user in userLeadership:     #change numbers into leadership ratings.
        user_score = userLeadership[user]
        user_percent = user_score / float(max_leader)
        user_rating = user_percent * 10
        user_rating_formatted = "{:.2f}".format(user_rating)
        userLeadership[user] = user_rating_formatted

    return


def calcTeams(data):
    commits = data.get('commits')   #grab all the commits
    userNames = []                  #holds the users involved with each commit
    codeLines = []                  #holds the lines of code involved with each commit
    analyzeThis = []                #holds the data to be passed into the clustering algorithm
    fileCount = len(fileVals)       #count the total number of files
    for comm in commits:            #for each commit:
        if comm[0] not in userTeamList:
            continue
        tempDict = {}               #create a temporary dictionary, which will hold the files.
        found = False               #tells us if any valid file was on this commit (thus avoiding useless commits)
        for f in fileVals:          #for each file in the list
            tempDict.update({f : 0})    #add it to the dictionary, set its value to 0 (meaning not used)
        for f in comm[5]:           #for each file in this commit
            if f in fileVals:       #if it is in the list
                found = True        #mark found as true (not a useless commit)
                tempDict.update({f : (fileCount)})  #update the dictionary value for that file
        if found:                   #if this commit isn't useless:
            branchvalue = branchVals[comm[4]]   #grab the branch value
            datevalue = dateVals[comm[1].split('T')[0]] #grab the datevalue
            commData = [branchvalue, datevalue]         #assign them both to an array
            for f in fileVals:                          #append the value of each file into the array
                commData.append(tempDict[f])
            analyzeThis.append(commData)                #add this array (for the commit) into the array of arrays (data to be clustered)
            userNames.append(comm[0])                   #add the appropriate user to the userlist under the same index.
            codeLines.append(comm[3])                   #add the appropriate lines of code to the codeLine array under the same index.
    ms = MeanShift(bandwidth=(fileCount * 1.4))         #Cluster the data.
    ms.fit(analyzeThis, y=None)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    n_clusters_ = len(np.unique(labels))

    #CLUSTERING TEST CODE:
    #print("Number of estimated clusters:", n_clusters_)
    #print(len(labels))
    #i = 0
    #testlist = []
    #for l in labels:
    #    print(l)
    #    if l != 0:
    #        testlist.append(i)
    #    i += 1
    #for v in testlist:
    #    tempitem = analyzeThis[v]
    #    print(userNames[v])
    #    print(commits[v][1])
    #    print(tempitem[1])
    #    print(tempitem[0])
    #    print(labels[v])
    #    print(tempitem)
    #END CLUSTERING TEST CODE

    userFileBreakdown = {}      #create a dictionary that's going to hold values for each file.. for each user.
    #Create dictionary entries for each user being examined for teammates
    for user in np.unique(userNames):       #for each (unique) user:
        tempDict = {}                       #create a dictionary for them
        for l in np.unique(labels):         #for each cluster:
            tempDict[l] = 0                 #make that cluster has a zero score in that dictionary
        tempDict['t'] = 0                   #add a total entry
        userFileBreakdown[user] = tempDict  #add the dictionary to the userFileBreakdown under the user's key
    i = 0   #used for accessing the correct index items
    #for each commit, add its total lines of code to the appropriate user and cluster.
    for l in labels:    #for each commit:
        name = userNames[i]     #grab the associated user
        lines = codeLines[i]    #grab the associate lines of code
        userFileBreakdown[(name)][l] += lines   #set the proper variable in the dictionary
        userFileBreakdown[(name)]['t'] += lines #also add to the total
        i += 1                                  #increment i
    #convert all the above values into percentages.
    for user in userFileBreakdown:              #for each key in the userFileBreakdown:
        total = userFileBreakdown[user]['t']    #grab the total
        for l in userFileBreakdown[user]:       #for each cluster, convert the value to a XX.XX percent
            lines = userFileBreakdown[user][l]
            percent = lines / float(total)
            percent_formatted = "{:.2f}".format(percent)
            userFileBreakdown[user][l] = float(percent_formatted)
    commonality_threshhold = 1 / ((len(contDict) - 1) * 2)  #determine a threshhold percentage that users must share to be considered teammates
    #determine teammates for each user
    for user in userFileBreakdown:  #grab a user from the list
        teammate_list = []          #initialize a list of their teamates.
        for user_iter in userFileBreakdown: #for each user in the list
            common = 0  #value used for determining similarities in their commits
            if user is user_iter:   #if the user is the same user, disregard them.
                continue
            for l in userFileBreakdown[user]:   #for each cluster:
                my_p = userFileBreakdown[user][l]   #grab the user's percentage.
                ur_p = userFileBreakdown[user_iter][l]  #grab the user we're comparing's percentage.
                same = min(my_p, ur_p)  #find out how much overlap they have
                common += same          #add the overlap value to the common variable
            if common >= commonality_threshhold:    #if they have enough in common
                teammate_list.append(user_iter)     #add that user to their teammate list
        userTeams[user] = teammate_list             #add this user's teammate list to the overarching dictionary
    for user in contDict:       #for each user
        if user in userTeams:   # if they DO have an entry in the teammate dictionary (Python is being stupid)
            something = 'if statements have to have something'  #then filler data cuz it doesn't matter
        else:   #if they DON'T (the important one)
            no = 'No Teammates' #set a variable
            userTeams[user] = no    #assign the value in the dictionary, so there is data there to reference.



def assignVals(data):
    #assign values to branches. These are to be large enough that they are definitely in different clusters.
    branchCount = 0
    for b in branchList:        #for each branch:
        branchVals[b] = branchCount     #assign it a value.
        branchCount += 500               #increment the value substantially.
    #determine values for all the commit dates.
    for d in dateList:          #for every date that a commit was made on
        date = convertDate(d)   #convert it to the format from convertDate.
        score = ((date[1] - startDate[1]) * 365) + (date[0] - startDate[0]) #calculate a score based on its location from the first commit's date.
        score = float(score) / 10000000  #divide that score by an amount that will vary how important dates are.
        dateVals[d] = score         #assign the value into the dateVals dict.
    return

def convertDate(date):
    #converts date as GitHub stores it into a useable format.
    formatted = date.split('-') #splits it in the way that GitHub stores it.
    months = {'01': 0, '02': 31, '03': 59, '04': 90, '05': 120, '06': 151, '07': 181, '08': 212, '09': 243, '10': 273, '11': 304, '12':334}
    #each month has a value. We are ignoring leap years for the negligible difference it makes.
    fdate = [months[formatted[1]] + int(formatted[2]), int(formatted[0])]   #the formatted date is [](day of year), (year)]
    return fdate    #return the newly formatted date

def calcContribution(data):
    #begin initialization
    total_score = 0         #keep track of a total throughout all non-private users.
    total_commits = 0
    total_codeLines = 0
    commits = data.get('commits')   #pull all commits out of our data
    comments = data.get('comments') #pull all comments out of our data
    for user in users:      #for each user:
        contDict[user] = 0      #initialize their contribution to 0
        userLangs[user] = []    #intiialize their languages to None
        branches = {}           #initialize their branches to None
        statsDict[user] = {'commitCount' : 0, 'codeLines' : 0, 'acceptedCommits' : 0, 'acceptedLines' : 0, 'commentCount' : 0, 'branches' : branches, 'filesLed' : 0, 'branchesLed' : 0}
        #userFileCounts[user] = {'default' : 0}  #initialize statsDict and userFileCounts to empty.
    branches = {}   #repeat the above process for a total user.
    bCount = []
    statsDict['-'] = {'commitCount' : 0, 'codeLines' : 0, 'acceptedCommits' : 0, 'acceptedLines' : 0, 'commentCount' : 0, 'branches' : branches, 'filesLed' : 0, 'branchesLed' : 0}
    #end initialization
    #begin languages for user
    for comm in commits:
        userLogin = comm[0]     #find the user's username
        if (userLogin != 'Private User') and (userLogin != 'web-flow'):     #assuming they aren't a private user:
            filenames = comm[5]     #get a list of all the filenames
            if comm[3] > 9:         #if they changed atleast 10 lines of code (that is, they made more than one small change)
                for f in filenames:     #check each file:
                    if f in fileVals:                   #if this is a file we keep track of:
                        fileLeaders[f][userLogin] += 1  #add to the total number of commits to this file this user has made.
                    extension = f.split('.')
                    e = extension[len(extension) - 1]   #obtain its file extension
                    if e in fileExtensions:                  #if it matches one
                        if fileExtensions[e] not in userLangs[userLogin]:   #and it isn't already in the list
                            userLangs[userLogin].append(fileExtensions[e])  #add the language to the user's list of languages.
    #end languages for user
    #begin contribution score & branches for user
            score = (comm[3] / float(6))    #calculate a base score, being total lines of code divided by 6 (what we consider 1 small change)
            total_score += score            #add this to the total score for the entire project.
            existingScore = contDict.setdefault(userLogin, 0)   #set this var to their score, or create their score and set it to zero if it didn't exist.
            contDict[userLogin] = existingScore + score         #add the new score to the existing score.
            statsDict[userLogin]['commitCount'] += 1            #add to the commitcount of the user by 1.
            total_commits += 1                                  #add to the total commits by 1.
            statsDict[userLogin]['codeLines'] += comm[3]        #add to the user's total lines of code changed.
            total_codeLines += comm[3]                          #add to the total amount of lines of code changed.
            branchLeaders[comm[4]][userLogin] += 1              #add to the total number of commits to this branch this user has made.
            if comm[4] not in statsDict[userLogin]['branches']: #if this branch isn't already in the user's list of used branches:
                statsDict[userLogin]['branches'].update({comm[4] : comm[3]})    #set the lines of code they've changed in that branch.
            else :                                                 #if it was already there:
                statsDict[userLogin]['branches'][comm[4]] += comm[3]    #add to the lines already there
    #end contribution score & branches for user
    #begin assigning scores
    for user in users:
        temp = contDict[user]   #grab the user's score
        cont_decimal = temp/float(total_score)  #convert into a percentage (decimal)
        cont_percent = "{:.2f}".format(cont_decimal * 100)  #convert into a percentage in format XX.XX - just add a %.
        contDict[user] = cont_percent   #reassign it back into the list.
    statsDict['-']['commitCount'] = total_commits   #assign the total user's values.
    statsDict['-']['codeLines'] = total_codeLines
    contDict['-'] = total_score
    #end assigning scores
    return 1;   #return.

def getExtensions():
    mariadb_connection = mariadb.connect(user='masterjam', password='jamfordays',host='myrd.csducou8syzm.us-east-1.rds.amazonaws.com', database='LanguageDB')
    cursor = mariadb_connection.cursor()
    cursor = mariadb_connection.cursor(buffered=True)
    query = "SELECT lang, extensions FROM languages"

    cursor.execute(query)
    mariadb_connection.commit()
    result = cursor.fetchall()
    print(result)
    return result;

def storePostAnalysisData(repoName, data):
    mariadb_connection = mariadb.connect(user='masterjam', password='jamfordays',host='myrd.csducou8syzm.us-east-1.rds.amazonaws.com', database='postAnalyzedDB')
    cursor = mariadb_connection.cursor()

    for user in data:
        username = user.get('userLogin')
        cont = user.get('contribution')
        lang = user.get('languages')
        langu = ''.join(lang)
        team = user.get('teams')
        teama= ''.join(team)
        lead = user.get('leadership')
        query ="DELETE FROM postData WHERE repositoryName = %s AND userName = %s"
        cursor.execute(query, (repoName, username))
        mariadb_connection.commit()
        sql = "INSERT INTO postData (repositoryName, userName, contribution, languages, teams, leadership) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (repoName, username, cont, langu, teama, lead))
        mariadb_connection.commit()
    return None
