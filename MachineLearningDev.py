from Authenticator import authenticate
from DataRetriever import getProjectData, getOrganizationData, getUsers, getRepoLanguages, getCommits, getMerges, getComments, getRepositories
from Analyzer import analyzeData, trainData
#import numpy as np
#from sklearn.cluster import MeanShift
#import matplotlib.pyplot as plt

if __name__ == '__main__':
    username = 'juicearific' #read username
    password = 'demopw123'  #read password
    #projname = 'torvalds/linux'
    projname = 'allisonsteinmetz/JAM'
    #projname = 'jpaugh/agithub'
    authToken = authenticate(username, password)
    projData = getProjectData(authToken, projname)
    data = analyzeData('dummyname', projData)

    #ms = MeanShift()
    #ms.fit(data)
    #labels = ms.labels_
    #cluster_centers = ms.cluster_centers_

    #n_clusters_ = len(np.unique(labels))

    #print("Number of estimated clusters:", n_clusters_)

    #colors = 10*['r.','g.','b.','c.','k.','y.','m.']

    #print(colors)
    #print(labels)

    #for i in range(len(X)):
    #    print(X[i][0])
    #    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

    #plt.scatter(cluster_centers[:,0], cluster_centers[:,1],
    #    marker = "x", s=150, linewidths = 5, zorder=10)

    #plt.show()


    for user in data:
        print(user.get('userLogin'))
        print(user.get('contribution'))
        print(user.get('uniqueStats').get('commitCount'))
        print(user.get('uniqueStats').get('codeLines'))
        branches = user.get('uniqueStats').get('branches')
        for branch in branches:
            print(branch)
        #for lang in user.get('languages'):
        #    print(lang)
