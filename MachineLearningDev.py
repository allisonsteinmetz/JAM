from Authenticator import authenticate
from DataRetriever import getProjectData, getOrganizationData, getUsers, getRepoLanguages, getCommits, getMerges, getComments, getRepositories
from Analyzer import analyzeData, trainData

if __name__ == '__main__':
    username = 'juicearific' #read username
    password = 'demopw123'  #read password
    authToken = authenticate(username, password)
    projData = getProjectData(authToken, 'allisonsteinmetz/JAM')
    analyzeData(projData)
