from flask import Flask, render_template, url_for,  redirect, request
from flask import make_response
from Navigator import search, select

pageURL = "/search"

@app.route('/search/')
