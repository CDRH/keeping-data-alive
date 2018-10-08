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
        # Allow alpha-nums, underscores, spaces, percents, periods, and hyphens
        child = re.search("\/[\w %.-]+$", container)
        if child != None:
            parent = re.sub("{0}$".format(child.group(0)), "", container)
        else:
            parent = ""

        # Handle space (%20) encoding
        container = re.sub(" ", "%20", container)
    else:
        parent = ""

    containers = []
    dae = json = log = mtl = obj = rpk = None

    g = rdflib.Graph()
    g.parse(fedora +"/"+ container)
    dae = json = log = mtl = obj = rpk = None
    for subj, pred, ob in g:
        if pred == ldp["#contains"]:
            path = re.sub(fedora, "", ob)
            containers.append(path)

            # Identify 3D model files
            if dae == None:
              dae = re.search("\.dae$", ob)
              if dae != None:
                  dae = dae.string

            if json == None:
              json = re.search("\.json$", ob)
              if json != None:
                  json = json.string

            if log == None:
              log = re.search("\.log$", ob)
              if log != None:
                  log = log.string

            if mtl == None:
              mtl = re.search("\.mtl$", ob)
              if mtl != None:
                  mtl = mtl.string

            if obj == None:
              obj = re.search("\.obj$", ob)
              if obj != None:
                  obj = obj.string

            if rpk == None:
              rpk = re.search("\.rpk$", ob)
              if rpk != None:
                  rpk = rpk.string

    # Prepare model dict for use in view
    if (dae != None) or (mtl != None and obj != None):
        model = {}

        if dae != None:
            model["dae"] = dae

        if json != None:
            model["json"] = json

        if log != None:
            model["log"] = log

        if (mtl != None and obj != None):
            model["mtl"] = mtl
            model["obj"] = obj

        if rpk != None:
            model["rpk"] = rpk
    else:
        model = None

    return dict(
        fedora=fedora,
        container=container,
        containers=containers,
        model=model,
        parent=parent
    )

# Prevents 500 error log spam from browser requests
@route("/favicon.ico")
def favicon():
    return ""

run(debug=True, host="localhost", port=3000, reloader=True)
