#!/usr/bin/env python

import argparse
import rdflib
import re


# Defaults
# --------
fedora = "https://cdrhdev1.unl.edu/fedora/rest"
LDP = rdflib.Namespace("http://www.w3.org/ns/ldp")



# Arguments
# ---------
parser = argparse.ArgumentParser()

# Optional args
parser.add_argument("-d", "--dry_run", action="store_true",
                    help="preview results; don't make any changes")
parser.add_argument("-q", "--quiet", action="store_true",
                    help="suppress output")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="verbose processing info")

# Positional args
parser.add_argument("container", default="/", help="Container path", nargs="?")

args = parser.parse_args()


# Assign args
container = args.container

# Ensure container begins with '/'
if re.search("^/", container) == None:
    container = "/"+ container



# Functions
# ---------
#def function_name(param):
    # Logic

#    return return_value



# Main
# ----
if  __name__ =='__main__':
    g = rdflib.Graph()
    g.parse(fedora + container)

    s = g.serialize(format='turtle')

    print "Fedora server: "+ fedora
    print "Container: "+ container

    print "Children (ldp#contains):"

    for subj, pred, obj in g:
        if pred == LDP['#contains']:
            print "  {0}".format(obj)

    if container == "/":
        print "Pass a container path as an argument to browse, e.g.:"
        print "  ./read_fedora.py /kda"
