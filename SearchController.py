from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response

passed = False

def getOrganizations(token, name):
    status, data = token.search.users.get(q = name)
    if status == 200:
        global passed
        passed = True
        items = data.get('items')
        orgs = []
        for org in items:
            orgs.append(org.get('login'))
        return orgs
        # returns a list of match org names
    else:
        return "Could not retrieve organizations"

def getProjects(token, name):
    status, data = token.search.repositories.get(q = name)
    if status == 200:
        global passed
        passed = True
        items = data.get('items')
        projects = []
        for item in items:
            projects.append(item.get('full_name'))
        return projects
        # returns a list of match project names
    else:
        return "Could not retrieve projects"
