from Authenticator import authenticate
from DataRetriever import getProjectData, getOrganizationData, getUsers, getRepoLanguages, getCommits, getMerges, getComments, getRepositories
from Analyzer import analyzeData
#import numpy as np
#from sklearn.cluster import MeanShift
#import matplotlib.pyplot as plt

if __name__ == '__main__':
    # username = 'juicearific' #read username
    # password = 'demopw123'  #read password
    # #projname = 'torvalds/linux'
    # projname = 'allisonsteinmetz/JAM'
    # #projname = 'jpaugh/agithub'
    # #projname = 'allisonsteinmetz/FamilyTreeCreator'
    # authToken = authenticate(username, password)
    # projData = getProjectData(authToken, projname)
    # data = analyzeData('dummyname', projData)

    real_user = 'juicearific'
    real_pass = 'demopw123'
    fake_user = 'fake_username'
    fake_pass = 'fake_password'
    real_name = 'allisonsteinmetz/JAM'
    real_proj_name = 'agithub'
    real_org_name = 'MyPureCloud'
    real_user_list = set(["allisonsteinmetz", "Juicearific", "MananVPatel"])
    fake_list = ['Analyzer.py', 'Analyzer.pyc', 'Authenticator.pyc', 'Navigator.py', 'SearchController.pyc']
    fake_commit = ('Juicearific', '2017-04-21T03:03:08Z', 'Presentation-Ready\n\n^title', 16, 'master', fake_list)
    fake_commits = [fake_commit, fake_commit]
    fake_comments =[]
    fake_repo_languages = []
    fake_data = {'users' : real_user_list, 'repoLanguages': fake_repo_languages,
        'commits': fake_commits, 'comments': fake_comments, 'merge' : 'WIP'}

    token = authenticate(real_user, real_pass)

    haspassed = analyzeData(' ', fake_data)
    print(haspassed)

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
        print(user.get('languages'))
        print(branches)
        print(user.get('uniqueStats').get('filesCreated'))
        #for lang in user.get('languages'):
        #    print(lang)
