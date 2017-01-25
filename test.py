import pytest
import Authenticator
import DataRetriever
import SearchController

#variables
real_user = 'juicearific'
real_pass = 'demopw123'
fake_user = 'fake_username'
fake_pass = 'fake_password'
real_name = 'allisonsteinmetz/JAM'
real_proj_name = 'agithub'
real_project_list = ['jpaugh/agithub', 'AGithub457/AGithub457.github.io', '37acoder/37Agithub', 'martinssegudo/RepositorioLocal', 'ahanekom/e4agithub', 'cs-abdulwahab/SecAGithubProjectDemo', 'NorthwestDeveloper/aGithubDemo']
real_user_list = set(["allisonsteinmetz", "Juicearific", "MananVPatel"])
real_orgs_list = ["MyPureCloud"]

token = Authenticator.authenticate(real_user, real_pass)
def test_auth():
    assert Authenticator.authenticate(real_user, real_pass) != False
    assert Authenticator.authenticate(fake_user, fake_pass) == False

def test_getProjectData():
    assert DataRetriever.getProjectData(token, real_name) == real_user_list

def test_searchProjects():
    SearchController.getProjects(token, real_proj_name)
    assert SearchController.passed == True

def test_searchOrganizations():
    SearchController.getOrganizations(token, 'MyPureCloud')
    assert SearchController.passed == True
