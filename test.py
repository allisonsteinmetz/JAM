import pytest
import Authenticator
import DataRetriever

#variables
real_user = 'juicearific'
real_pass = 'demopw123'
fake_user = 'fake_username'
fake_pass = 'fake_password'
real_name = 'allisonsteinmetz.JAM'
real_user_list = set(["allisonsteinmetz", "Juicearific", "MananVPatel"])

token = Authenticator.authenticate(real_user, real_pass)
def test_auth():
    assert Authenticator.authenticate(real_user, real_pass) != False
    assert Authenticator.authenticate(fake_user, fake_pass) == False

def test_getProjectData():
    assert DataRetriever.getProjectData(token, real_name) == real_user_list
