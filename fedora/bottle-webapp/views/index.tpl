<!DOCTYPE html>
<html lang="en" data-suburi="{{suburi}}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script
      crossorigin="anonymous"
      integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
      src="https://code.jquery.com/jquery-3.3.1.min.js"
    ></script>
    <link
      crossorigin="anonymous"
      href="https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
      integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
      rel="stylesheet"
    >
    <script
      crossorigin="anonymous"
      integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"
      src="https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
    ></script>
    <script src="{{suburi}}/js/lib/three.min.js"></script>
    <script src="{{suburi}}/js/lib/OrbitControls.js"></script>
    <script src="{{suburi}}/js/three-viewer.js"></script>
    <title>
      Fedora Viewer
    </title>
  </head>
  <body class="container-fluid">
    <h1>Fedora Viewer</h1>

    <p>
      <strong>Server:</strong>
      {{fedora}}
    </p>

    %if container != "":
      <p>
        <strong>Parent:</strong>
        <a class="btn btn-warning" href="{{suburi}}/{{parent}}">/{{parent}}</a>
      </p>
    %end

    <p>
      <strong>Container:</strong>
      <span class="well well-sm">/{{container}}</span>

      <ul>
        %for c in containers:
          <li>
            <a class="btn btn-primary" href="{{suburi}}{{c}}">
              {{c}}
            </a>
          </li>
        %end
      </ul>
    </p>

    %if model != None:
      <div class="row">
        <div class="col-md-6">
          <h2>3D View</h2>
          <div class="well model-viewer">
          </div>

          <h3>Controls:</h3>
          <p>
            Left-click and drag to pan the camera<br>
            Right-click and drag to move the camera's focal point<br>
            Scroll the mouse wheel to zoom in and out
          </p>
        </div>

        <div class="col-md-6">
          <h3>Files</h3>
          <ul>
            <li>
              <strong>Model File(s):</strong>
              <ul>
                %if model.has_key("dae"):
                  <li class="dae">{{model["dae"]}}</li>
                %end
                %if model.has_key("obj"):
                  <li class="obj">{{model["obj"]}}</li>
                %end
               </ul>
            </li>
            %if model.has_key("jpg") or model.has_key("mtl") or model.has_key("png"):
              <li>
                <strong>Texture File(s):</strong><br>
                Note: TIFFs are not supported by Three.js
                <ul>
                  %if model.has_key("jpg"):
                    %for jpg in model["jpg"]:
                      <li class="jpg">{{jpg}}</li>
                    %end
                  %end
                  %if model.has_key("mtl"):
                    <li class="mtl">{{model["mtl"]}}</li>
                  %end
                  %if model.has_key("png"):
                    %for png in model["png"]:
                      <li class="png">{{png}}</li>
                    %end
                  %end
                </ul>
              </li>
            %end
            %if model.has_key("json"):
              <li>
                <strong>Metadata:</strong>
                <ul>
                  <li>{{model["json"]}}</li>
                </ul>
              </li>
            %end
            %if model.has_key("log") or model.has_key("rpk"):
              <li>
                <strong>City Engine Data:</strong>
                <ul>
                  %if model.has_key("log"):
                    <li>{{model["log"]}}</li>
                  %end
                  %if model.has_key("rpk"):
                    <li>{{model["rpk"]}}</li>
                  %end
                </ul>
              </li>
            %end
          </ul>
        </div>
      </div>
    %end
  </body>
</html>
