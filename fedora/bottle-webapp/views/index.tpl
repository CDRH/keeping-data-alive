<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
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
        <a class="btn btn-warning" href="/{{parent}}">/{{parent}}</a>
      </p>
    %end

    <p>
      <strong>Container:</strong>
      <span class="well well-sm">/{{container}}</span>

      <ul>
        %for c in containers:
          <li>
            <a class="btn btn-primary" href="{{c}}">
              {{c}}
            </a>
          </li>
        %end
      </ul>
    </p>

    %if model != None:
      <div>
        <h2>3D View</h2>
        <div>
        </div>

        <h3>Files</h3>
        <ul>
          <li>
            <strong>Model File(s):</strong>
            <ul>
              %if model.has_key("dae"):
                <li>{{model["dae"]}}</li>
              %end
              %if model.has_key("mtl") and model.has_key("obj"):
                <li>{{model["mtl"]}}</li>
                <li>{{model["obj"]}}</li>
              %end
             </ul>
          </li>
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
    %end
  </body>
</html>
