import pytest
import GitHubCommunicator

#variables
real_user = 'juicearific'
real_pass = 'demopw123'
fake_user = 'fake_username'
fake_pass = 'fake_password'
real_user_list = ["allisonsteinmetz", "Juicearific", "MananVPatel"]

def test_auth():
    assert GitHubCommunicator.authenticate(real_user, real_pass) != False
    assert GitHubCommunicator.authenticate(fake_user, fake_pass) == False

def test_getUsers():
    g = GitHubCommunicator.authenticate(real_user, real_pass)
    assert GitHubCommunicator.getUsers(g) == real_user_list