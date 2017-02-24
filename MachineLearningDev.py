from Authenticator import authenticate
from DataRetriever import getProjectData, getOrganizationData, getUsers, getRepoLanguages, getCommits, getMerges, getComments, getRepositories
from Analyzer import analyzeData, trainData

if __name__ == '__main__':
    username = 'juicearific' #read username
    password = 'demopw123'  #read password
    projname = 'torvalds/linux'
    projname = 'allisonsteinmetz/JAM'
    #projname = 'jpaugh/agithub'
    authToken = authenticate(username, password)
    projData = getProjectData(authToken, projname)
    data = analyzeData(projData)
    for user in data:
        print(user.get('userLogin'))
        print(user.get('contribution'))
        for lang in user.get('languages'):
            print(lang)
