from agithub.GitHub import GitHub
from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response

def getOrganizations(token, name):
    status, data = token.search.repositories.get(q = name)
    if status == 200:
        items = data.get('items')
        projects = []
        for item in items:
            projects.append(item.get('full_name'))
        return projects
    else:
        return "Could not retrieve organizations"
    #this is for the search page
    #find relevant orgs, return them.

def getProjects(token, name):
    #this is for the search page
    #find relevant projects, return them.
    return None
