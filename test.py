import pytest
import Authenticator
import DataRetriever
import SearchController
import Analyzer

#variables
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

token = Authenticator.authenticate(real_user, real_pass)
def test_auth():
    assert Authenticator.authenticate(real_user, real_pass) != False
    assert Authenticator.authenticate(fake_user, fake_pass) == False

def test_getProjectData():
    DataRetriever.getProjectData(token, real_name)
    assert DataRetriever.passed == True

def test_getOrganizationData():
    DataRetriever.getProjectData(token, real_name)
    assert DataRetriever.passed == True

def test_searchProjects():
    SearchController.getProjects(token, real_proj_name)
    assert SearchController.passed == True

def test_searchOrganizations():
    SearchController.getOrganizations(token, real_org_name)
    assert SearchController.passed == True

def test_analysis():
    haspassed = Analyzer.analyzeData(' ', fake_data)
    assert haspassed == [{'userLogin': 'MananVPatel', 'teams': 'No Teammates', 'languages': [], 'leadership': '0.00', 'uniqueStats': {'commentCount': 0, 'branchesLed': 0, 'filesCreated': 0, 'branches': 0, 'filesLed': 0, 'acceptedLines': 0, 'acceptedCommits': 0, 'codeLines': 0, 'commitCount': 0}, 'contribution': '0.00'}, {'userLogin': 'allisonsteinmetz', 'teams': 'No Teammates', 'languages': [], 'leadership': '0.00', 'uniqueStats': {'commentCount': 0, 'branchesLed': 0, 'filesCreated': 0, 'branches': 0, 'filesLed': 0, 'acceptedLines': 0, 'acceptedCommits': 0, 'codeLines': 0, 'commitCount': 0}, 'contribution': '0.00'}, {'userLogin': 'Juicearific', 'teams': [], 'languages': ['Python'], 'leadership': '10.00', 'uniqueStats': {'commentCount': 0, 'branchesLed': 1, 'filesCreated': 2, 'branches': 0, 'filesLed': 2, 'acceptedLines': 0, 'acceptedCommits': 0, 'codeLines': 32, 'commitCount': 2}, 'contribution': '100.00'}, {'userLogin': '-', 'teams': 'No Teammates', 'languages': '', 'leadership': '10.00', 'uniqueStats': {'commentCount': 0, 'branchesLed': 0, 'filesCreated': 2, 'branches': 0, 'filesLed': 0, 'acceptedLines': 0, 'acceptedCommits': 0, 'codeLines': 32, 'commitCount': 2}, 'contribution': 5.333333333333333}]
