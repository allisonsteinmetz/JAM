GitHub_API = "https://api.github.com"

import requests, time
import json
import os
import Globalss
from urlparse import urljoin
from requests.auth import HTTPBasicAuth
from agithub.GitHub import GitHub

username = raw_input('Github username: ')
password = raw_input('password: ')
msg = ""
#JAM_SECRET = 'test1'
#secret = os.environ['JAM_SECRET']
#id = os.environ['JAM_CLIENT_ID']

def getAuthCode():
    authorization_code_req = {
        "response_typpe" : "code",
        "client_id" : client_id,
        "redirect_uri": redirect_uri,
        "scope": ("https://www.google.com")
    }

    r = requests.get(base_url + "auth?%s" % urlencode(authorization_code_req),
        allow_redirects=False)

def main():
    g = GitHub(username, password)
    status, data = g.issues.get(filter='subscribed', foobar='llama')
    print(status)
    print(g.repos.allisonsteinmetz.JAM.contributors.get())
    # url = urljoin(GitHub_API, "authorizations")
    # print(url)
    # payload = {}
    # res = requests.post (
    #     "https://github.com/login/oauth/authorize?client_id=060bd7a32bdca5ebda07",
    #     auth = HTTPBasicAuth(username, password),
    #     data = json.dumps(payload),
    # )
    # print(res.text)
    # j = json.loads(res.text)
    # if res.status_code >= 400:
    #     msg = j.get('message', 'UNDEFINED ERROR (no error description from server)')
    #     print ('error: %s' %msg)
    #     return
    # token = j['token']
    # print ('New token: %s' % token)

#if __name__ == '__main__':
main()
