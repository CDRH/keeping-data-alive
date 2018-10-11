#!/usr/bin/env python

from bottle import route, run, static_file, template, view
import bottle
import os
import rdflib
import re


# Config
# ------
app = bottle.default_app()
app.config["fedora"] = "http://cdrhdev1.unl.edu/fedora/rest"
app.config["ldp"] = rdflib.Namespace("http://www.w3.org/ns/ldp")


# Routes
# ------
@route("/js/<filepath:path>")
def js(filepath):
    js_path = os.path.dirname(os.path.realpath(__file__)) +"/js"
    return static_file(filepath, root=js_path)

@route("/raw/<filepath:path>")
def raw(filepath):
    raw_path = os.path.dirname(os.path.realpath(__file__)) +"/raw"
    return static_file(filepath, root=raw_path)

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

    # Variables
    # Lists assigned separately, otherwise variables point to the same list
    containers = []
    dae = json = log = mtl = obj = rpk = None
    jpg = []
    png = []

    g = rdflib.Graph()
    g.parse(fedora +"/"+ container)
    for subj, pred, ob in g:
        if pred == ldp["#contains"]:
            # Remove base of URL for less redundant display
            path = re.sub(fedora, "", ob, flags=re.I)
            containers.append(path)

            # Store model files
            if dae == None:
              dae = re.search("\.dae$", ob, flags=re.I)
              if dae != None:
                  dae = dae.string

            if obj == None:
              obj = re.search("\.obj$", ob, flags=re.I)
              if obj != None:
                  obj = obj.string

            # Store texture files
            # May be multiple JPGs
            jpg_search = re.search("\.jpe?g$", ob, flags=re.I)
            if jpg_search != None:
                jpg.append(jpg_search.string)

            if mtl == None:
              mtl = re.search("\.mtl$", ob, flags=re.I)
              if mtl != None:
                  mtl = mtl.string

            # May be multiple PNGs
            png_search = re.search("\.png$", ob, flags=re.I)
            if png_search != None:
                png.append(png_search.string)

            # Store metadata file
            if json == None:
              json = re.search("\.json$", ob, flags=re.I)
              if json != None:
                  json = json.string

            # Store City Engine files
            if log == None:
              log = re.search("\.log$", ob, flags=re.I)
              if log != None:
                  log = log.string

            if rpk == None:
              rpk = re.search("\.rpk$", ob, flags=re.I)
              if rpk != None:
                  rpk = rpk.string

    # Prepare model dict for use in view
    if dae != None or obj != None:
        model = {}

        # Single files
        if dae != None:
            model["dae"] = dae

        if json != None:
            model["json"] = json

        if log != None:
            model["log"] = log

        if mtl != None:
            model["mtl"] = mtl

        if obj != None:
            model["obj"] = obj

        if rpk != None:
            model["rpk"] = rpk

        # File lists
        if len(jpg) > 0:
            model["jpg"] = jpg

        if len(png) > 0:
            model["png"] = png
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
