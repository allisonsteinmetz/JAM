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
fake_commit = ('User1', 'date', 'msg', 12)
fake_commits = []
fake_comments =[]
fake_repo_languages = []
fake_data = {'users' : list(set('User1')), 'repoLanguages': fake_repo_languages,
    'commits': fake_commits, 'comments': fake_comments}

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

def test_contribution():
    haspassed = Analyzer.calcContribution(fake_data)
    assert haspassed == True
