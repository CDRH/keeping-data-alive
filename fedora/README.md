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
  - [Fedora](#fedora)
    - [Adding Data](#adding-data)
    - [Deleting Data](#deleting-data)
  - [Scripts](#scripts)
    - [read_fedora.py](#read_fedorapy)
  - [Bottle Webapp](#bottle-webapp)

## Server Software

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

`./read_fedora.py [container_path(default="/")]`


### Bottle Webapp
Bottle web app to browse Fedora repository containers

`./fedora.py`

Visit `http://localhost:3000`
