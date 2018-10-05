#!/usr/bin/env python

from bottle import route, run, template, view
import bottle
import rdflib
import re


# Config
# ------
app = bottle.default_app()
app.config["fedora"] = "http://cdrhdev1.unl.edu/fedora/rest"
app.config["ldp"] = rdflib.Namespace("http://www.w3.org/ns/ldp")


# Routes
# ------
@route("/")
@route("/<container:path>")  # :path captures whole value including /'s
@view("index")
def index(container=""):
    fedora = app.config["fedora"]
    ldp = app.config["ldp"]

    if container != "":
        child = re.search("\/\w+$", container)
        if child != None:
            parent = re.sub("{0}$".format(child.group(0)), "", container)
        else:
            parent = ""
    else:
        parent = ""

    containers = []
    g = rdflib.Graph()
    g.parse(fedora +"/"+ container)
    for subj, pred, obj in g:
        if pred == ldp["#contains"]:
            path = re.sub(fedora, "", obj)
            containers.append(path)

    return dict(
        fedora=fedora,
        container=container,
        containers=containers,
        parent=parent
    )

# Prevents 500 error log spam from browser requests
@route("/favicon.ico")
def favicon():
    return ""

run(debug=True, host="localhost", port=3000, reloader=True)
