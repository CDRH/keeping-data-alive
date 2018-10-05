# Fedora

**Contents**

- [Dependencies](#dependencies)
  - [Common](#common)
    - [RDFLib](#rdflib)
  - [Bottle](#bottle)
- [Usage](#usage)
  - [Scripts](#scripts)
    - [read_fedora.py](#read_fedorapy)
  - [Bottle Webapp](#bottle-webapp)

## Dependencies

### Common

#### RDFLib
The python code requires the RDFLib library

**Fedora**

`sudo dnf install python-rdflib`

**EL**

`sudo yum install python-rdflib`

**Pip**

`sudo pip install rdflib`

### Bottle

**Fedora**

`sudo dnf install python-bottle`

**EL**

`sudo yum install python-bottle`

**Pip**

`sudo pip install bottle`


## Usage

### Scripts

#### read_fedora.py
Command line script to print out containers from Fedora repository

`./read_fedora.py [container_path(default="/")]`


### Bottle Webapp
Bottle web app to browse Fedora repository containers

`./fedora.py`

Visit `http://localhost:3000`
