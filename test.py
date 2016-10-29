GitHub_API = "Https://api.github.com"

import requests, time
import json
import os
import Globalss
from urllib.parse import urljoin


username = input('Github username: ')
password = input('password: ')
msg = ""
#JAM_SECRET = 'test1'
#secret = os.environ['JAM_SECRET']
#id = os.environ['JAM_CLIENT_ID']

def getAuthCode():
    authorization_code_req = {
        "response_typpe" : "code",
        "client_id" : client_id,
        "redirect_uri": redirect_uri,
        "scope": (r"https://www.google.com")
    }

    r = requests.get(base_url + "auth?%s" % urlencode(authorization_code_req),
        allow_redirects=False)

def main():
    url = urljoin(GitHub_API, "Authorization")
    payload = {}
    res = requests.post (
        url,
        auth = (username, password),
        data = json.dumps(payload),
    )
    j = json.loads(res.text)
    if(res.status_code >= 400
        msg = j.get('message', 'UNDEFINED ERROR (no error description from server)')
        print ('error: %s' %msg)
        return
    token = j['token']
    print ('New token: %s' % token)

if __name__ == '__main__':
    main()
