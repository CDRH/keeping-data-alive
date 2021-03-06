# Fedora

**Contents**

- [Server Software](#server-software)
  - [Apache Tomcat](#apache-tomcat)
  - [Fedora Repository](#fedora-repository)
    - [Tomcat Reverse Proxy](#tomcat-reverse-proxy)
- [Dependencies](#dependencies)
  - [Common](#common)
    - [RDFLib](#rdflib)
  - [Bottle](#bottle)
- [Usage](#usage)
  - [Fedora](#fedora-1)
    - [Adding Data](#adding-data)
    - [Deleting Data](#deleting-data)
  - [Scripts](#scripts)
    - [read_fedora.py](#read_fedorapy)
  - [Bottle Webapp](#bottle-webapp)
    - [Standalone](#standalone)
    - [WSGI](#wsgi)

## Server Software

Note these instructions are intended to help set up this proof of concept
software environment on your own development machine or server. This is why we
use example URLs like http://localhost:8080/ and http://host.domain.tld/, which
may differ for your environment.

### Apache Tomcat
We used Tomcat 8.5 to deploy the Fedora web application.

Tomcat depends on [Java](https://java.com/en/) which may be installed from the official site or via:

DNF/YUM|APT|[Homebrew](https://brew.sh/)
-------|---|--------
`sudo dnf install java-openjdk`|`sudo apt-get install default-jdk`|`brew cask install java`

[Tomcat 8.5 Downloads](https://tomcat.apache.org/download-80.cgi)

[Tomcat 8.5 Install Documentation](https://tomcat.apache.org/tomcat-8.5-doc/RUNNING.txt)

Though the version may differ, Tomcat may also be installed via:

DNF/YUM|APT|[Homebrew](https://brew.sh/)
-------|---|--------
`sudo dnf install tomcat`|`sudo apt-get install tomcat`|`brew install tomcat`

### Fedora Repository
[Fedora Downloads](https://duraspace.org/fedora/download/)

We used the "Web Application" variant of [Fedora 4.7.5](https://github.com/fcrepo4/fcrepo4/releases/download/fcrepo-4.7.5/fcrepo-webapp-4.7.5.war)

Note that the name of this `.war` file determines which sub-URI of Apache Tomcat
the Fedora Repository software will be accessible at when deployed. We recommend
renaming the file to `fedora.war` before moving it into Tomcat's `webapps/`
directory for this reason. This will result in the Fedora Repository being
accessible at http://localhost:8080/fedora/, like in our example URLs.

[Fedora Installation Instructions](https://wiki.duraspace.org/display/FEDORA475/Deploying+Fedora+4+Complete+Guide#DeployingFedora4CompleteGuide-DeployingwithTomcat7)

Especially note the step to add Fedora config options to the Tomcat startup environment which configures where Fedora data will be stored via the `fcrepo.home` option (e.g.)
`sudo vim /path/to/tomcat/bin/setenv.sh`:
```bash
# Configure Tomcat Environment
##############################

# Apps
######
FCREPO="-Dfcrepo.modeshape.configuration=classpath:/config/file-simple/repository.json -Dfcrepo.home=/var/local/fedora-data"

# Memory
########
# Min Overall
MEM_MIN="128m"

# Max Overall
MEM_MAX="2g"


# Set Environment
export CATALINA_OUT=/var/log/tomcat/catalina.out
export CATALINA_PID=/var/run/tomcat-catalina.pid
export JAVA_OPTS="-Dfile.encoding=UTF-8 -Xms${MEM_MIN} -Xmx${MEM_MAX} ${FCREPO}"
```

#### Tomcat Reverse Proxy
If one wants to reverse proxy the Tomcat webapp through Apache at a sub-URI (e.g. `https://host.domain.tld/fedora/`) as we did, additional Tomcat and Apache configuration is necessary due to the webapp generating links that Apache can't rewrite via mod_proxy_html, mod_rewrite, and mod_substitute. In this case, we must deploy the webapp separately from the drop-in auto-deploy directory `/path/to/tomcat/webapps` and utilize a custom Connector added to the Tomcat server config in `/path/to/tomcat/conf/server.xml`.

Add a reverse proxy Connector to Tomcat server config

`sudo vim /path/to/tomcat/conf/server.xml`:
```xml
…
  <Service name="Catalina">
…
    <!-- Reverse proxy connector -->
    <Connector port="8081" protocol="HTTP/1.1"
               connectionTimeout="20000"
               proxyName="hostname" proxyPort="80" />
…
    <Engine name="Catalina" defaultHost="localhost">
…
    </Engine>
  </Service>
</Server>
```

Place the webapp's .war file in a new, separate directory such as `/path/to/tomcat/proxied-webapps/` and define the webapp's Context XML file for deployment. Be careful that the .war file should be re-named the same as your sub-URI and Context's path values. For our purposes, the file should be re-named `fedora.war`, so that it unpacks to the directory `/path/to/tomcat/proxied-webapps/fedora/`.

`sudo vim /path/to/tomcat/Catalina/localhost/fedora.xml`:
```xml
<Context docBase="/path/to/tomcat/proxied-webapps/fedora"
  path="/fedora" reloadable="false" useHttpOnly="true"></Context>
```

Add the reverse-proxy configuration to Apache paying extra attention to proxy traffic to port 8081 rather than 8080

`sudo vim /path/to/apache/conf.d/fedora.conf`:
```ini
RedirectMatch ^/fedora$ /fedora/

<Location /fedora/>
  # Reverse proxy to serve example webapp requests
  # Port 8081 reverse-proxies with consisent app-generated URLs
  ProxyPass http://(ServerName):8081/fedora
  ProxyPassReverse /
</Location>
```

Some additional directives may still be necessary to fix `http://` and doubled sub-URIs in URLs

`sudo vim /path/to/apache/conf.d/fedora.conf`:
```ini
…
<Location /fedora/>
  …
  # Use mod_substitute to fix http:// in URLs
  AddOutputFilterByType SUBSTITUTE text/html text/plain
  Substitute s|http://(ServerName)|https://(ServerName)|

  # Fix doubled sub-URIs
  RewriteRule /fedora/fedora/(.*) /fedora/$1 [L,R]
</Location>
```

## Dependencies

### Common

#### RDFLib
The python code requires the RDFLib library

Fedora|EL|Pip
------|--|---
`sudo dnf install python-rdflib`|`sudo yum install python-rdflib`|`sudo pip install rdflib`


### Bottle

Fedora|EL|Pip
------|--|---
`sudo dnf install python-bottle`|`sudo yum install python-bottle`|`sudo pip install bottle`


## Usage

### Fedora

#### Adding Data
Testing files were generated with the [CityEngine Export Workflow](https://github.com/CDRH/keeping-data-alive/tree/master/workflow1) and added to separate containers via the Fedora REST API web interface's "Create New Child Resource" form, available at http://localhost:8080/fedora/rest/ or https://host.domain.tld/fedora/rest/ depending on whether one deploys Tomcat standalone or through Apache.

Each container's **Identifier** value may differ from the exported file names, so feel free to be descriptive or more brief for some of the longer model names. Click the **Add** button at the bottom of the form. The container should be created and its page loaded.

Repeat these steps until all exported files have been added:

- From the **Type** select, choose "Binary"
- For the **Identifier**, enter the full file name including extension
- Click the **File** button and select the matching file
- Click the **Add** button below
- To add another file to the same container, click the parent container's name in the gray bar with breadcrumb links just below the large page header with the current URL

If there are individual models nested within an export's files or textures stored within subdirectories, create containers with **Identifier** values that match the subdirectory names exactly.

#### Deleting Data

If one wants to permanently delete a resource from the Fedora repository or re-use a previously deleted resource, Fedora's [tombstone](https://wiki.duraspace.org/display/FEDORA40/Glossary#Glossary-Tombstone) resource must be deleted first. This is a resource Fedora creates in the background any time a resource is deleted or moved to prevent a URL from ever representing more than one resource. We aren't using Fedora as a permanent repository yet though, so we may want to do this.

If we create a container resource with the **Identifier** `derp`, delete it, then visit its URL `/fedora/rest/derp`, we'll be presented with this plaintext response:
```
Discovered tombstone resource at /derp, departed: 2018-10-12T18:42:09.684-05:00
```

One may delete this resource with `curl` via the command line:
```bash
curl -X DELETE http://localhost:8080/fedora/rest/derp/fcr:tombstone
```

or one may use Firefox's Network Monitor development tool:

- Visit the tombstone URL http://localhost:8080/fedora/rest/derp/fcr:tombstone
- Open Network Monitor via keyboard shortcut with `Ctrl + Shift + E` or
  `Command + Option + E`
- Click the row with `fcr:tombstone` under the File column
- Click "Edit and Resend" in the pane opened to the right
- Replace the `GET` method with `DELETE`
- Click "Send" in the upper right corner of the New Request pane

Now, if one tries to visit the URL `/fedora/rest/derp`, a Tomcat 404 error page should be returned. This means the tombstone resource has been successfully deleted. The identifier may remain permanently deleted or be re-used now.


### Scripts

#### read_fedora.py
Command line script to print out containers from Fedora repository

Near the top of the script, ensure this line defines the URL at which your
Fedora Repository is accessible:
```
fedora = "http://localhost:8080/fedora/rest"
```

Then run the script as follows:

`./read_fedora.py [container_path(default="/")]`

Running the script with no argument will display the containers present at the root of the Fedora repository. The script will print a message suggesting how to pass container paths in this case.

This script was written to determine how to retrieve information from the Fedora repository based on RDF relationships. The python RDFLib library understands multiple RDF formats, including the Turtle format returned to requests to Fedora. This script only prints the objects of tuples which use one Turtle predicate, `ldp#contains`, but the code could easily be modified to handle other RDF relationships including those from PCDM, Dublin Core, and Europeana Data Model. The code written to parse the Turtle responses is based on the [RDFLib Getting Started](https://rdflib.readthedocs.io/en/stable/gettingstarted.html) examples.

Note the script is not programmed to handle paths for Binary resources, such as 3D model, image, and text files. Entering paths for these will result in an error like `rdflib.plugin.PluginException: No plugin registered for (image/tiff, <class 'rdflib.parser.Parser'>)`.

### Bottle Webapp
Bottle web app to browse Fedora repository containers

The web app may be run as a standalone program served at port 3000 (typically for local development), or via a WSGI-compatible web server such as via Apache + mod_wsgi.

Near the top of `fedora.py`, ensure this line defines the URL at which your
Fedora Repository is accessible:
```
app.config["fedora"] = "http://localhost:8080/fedora/rest"
```

The app may be configured to serve from a sub-URI by defining the sub-URI in a `settings.ini` file placed in the same directory as the example `settings.example.ini` file and `app.wsgi`. If `settings.ini` is not present, the app will assume it is running at the root of the host's web space.

#### Standalone
`./run.py`

Logging and errors are output to this terminal.

Visit `http://localhost:3000`.

#### WSGI
The web app will deploy to any WSGI-compatible web server.

We provide an example configuration of serving the app at the `/fedora-viewer/` sub-URI via Apache + mod_wsgi here:

`settings.ini`:
```ini
[fedora]
suburi=fedora-viewer
```

```conf
RedirectMatch ^/fedora-viewer$ /fedora-viewer/

WSGIDaemonProcess fedora user=apache group=apache processes=1 threads=5
WSGIScriptAlias /fedora-viewer /var/local/www/python/keeping-data-alive/fedora/bottle-webapp/app.wsgi

<Location /fedora-viewer/>
  Require all granted
</Location>

<Directory /var/local/www/python/keeping-data-alive/fedora/bottle-webapp>
  WSGIProcessGroup fedora
  WSGIApplicationGroup %{GLOBAL}

  Require all granted
</Directory>
```


The Bottle web app was written to demonstrate the ability to retrieve and browse the same RDF data from Fedora, as well as identify 3D model files and render them for viewing within a browser. The page was written with Bootstrap so it is mobile-friendly.

Rendering the 3D models is achieved by parsing the list of resources within a LDP container for identifiers indicating file types by extensions, e.g. `.dae`, `.obj`, `.jpg`, `.json`, etc. When a `.dae` or `.obj` file is encountered, the page will render a [three.js](https://threejs.org) viewer and load the model and any accompanying textures. Collada (`.dae`) files contain paths to their textures and three.js will load them automatically. `.obj` files however use an addition `.mtl` file to render their textures. three.js supports loading textures for application to `.obj` models, but this has not been implemented yet. The necessary [MTLLoader.js](https://github.com/CDRH/keeping-data-alive/blob/master/fedora/bottle-webapp/js/lib/MTLLoader.js) library has been included in the [JavaScript files](https://github.com/CDRH/keeping-data-alive/tree/master/fedora/bottle-webapp/js/lib) and implementation would be based on the [three.js OBJLoader + MTLLoader example](https://github.com/mrdoob/three.js/blob/master/examples/webgl_loader_obj_mtl.html). In the mean time, all image texture files present alongside a `.obj` file are loaded and randomly applied to the faces of the model. Note that TIFF images are not supported by three.js.

The Bottle web app also is not programmed to handle loading Binary resources when requested through the buttons used to browse the Fedora repository. Clicking these links will return `Error: 500 Internal Server Error` messages.
