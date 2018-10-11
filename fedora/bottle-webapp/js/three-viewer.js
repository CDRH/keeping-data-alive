// Code adapted from:
// https://github.com/mrdoob/three.js/blob/master/examples/webgl_loader_obj.html
// https://github.com/mrdoob/three.js/blob/dev/examples/webgl_loader_collada.html
// https://github.com/mrdoob/three.js/blob/dev/examples/webgl_loader_collada_skinning.html

$(function () {
  // Check if a 3D model is present
  if ($(".dae").length > 0 || $(".obj").length > 0) {
    // Common variables
    var
      camera,
      model_url,
      mouseX = 0,
      mouseY = 0,
      object,
      renderer,
      scene = new THREE.Scene(),
      textures = [],
      viewer = $(".model-viewer")[0],
      viewH = 480,
      viewW = viewer.clientWidth - 40
    ;

    // Common functions
    function animate() {
      requestAnimationFrame( animate );
      renderer.render( scene, camera );
    }

    function loadTextures() {
      var images = [];
      if ($(".jpg").length > 0) {
        $(".jpg").each(function () {
          images.push(this.innerText);
        });
      }
      else if ($(".png").length > 0) {
        $(".png").each(function () {
          images.push(this.innerText);
        });
      }

      // If no texture from Fedora, use local default
      if (! images.length) {
        textures = [textureLoader.load("/raw/unknowntexture.png")];
      }
      else {
        for (var i in images) {
          textures.push(textureLoader.load(images[i]));
        }
      }
    }

    function loadModel() {
      if (object !== undefined) {
        // Apply textures to OBJ models randomly while not using MTL
        if ($(".obj").length > 0) {
          textureCount = textures.length;

          object.traverse(function (node) {
            if ( node.isMesh ) {
              randomIndex = Math.floor(Math.random() * textureCount)
              node.material.map = textures[randomIndex];
            }
          });
        }

        // Alter vertical position of object within scene
        object.position.y = 0;

        scene.add( object );
      }
    }

    function onError( error ) {
      console.log( "Couldn't download model from "+ model_url );
    }

    function onLoaderProgress( item, loaded, total ) {
      console.log( "Resource", loaded, "of", total );
      console.log( "  Loaded: "+ item );
    };

    function onProgress( xhr ) {
      if ( xhr.lengthComputable ) {
        var percentComplete = xhr.loaded / xhr.total * 100;
        console.log( "Model " + Math.round( percentComplete, 2 ) + "% downloaded" );
      }
    }

    // Camera
    camera = new THREE.PerspectiveCamera( 5, viewW / viewH, 1, 10000 );
    camera.position.x = -250;
    camera.position.y = 150;
    camera.position.z = -250;
    camera.zoom = 1;
    camera.updateProjectionMatrix();

    var pointLight = new THREE.PointLight( 0xffffff, 0.8 );
    camera.add( pointLight );

    scene.add( camera );

    // Ambient Light
    var ambientLight = new THREE.AmbientLight( 0xcccccc, 0.4 );
    scene.add( ambientLight );

    // Grid
    var grid = new THREE.GridHelper( 1200, 60, 0xFF4444, 0x404040 );
    scene.add( grid );

    // Loading Manager & Texture Loader
    var manager = new THREE.LoadingManager( loadModel );
    manager.onProgress = onLoaderProgress;
    var textureLoader = new THREE.TextureLoader( manager );

    // Determine model loader to use
    if ($(".dae").length > 0) {
      $.getScript("/js/lib/ColladaLoader.js", function () {
        // Model and Textures
        // ColladaLoader handles textures internally
        var loader = new THREE.ColladaLoader( manager );
        model_url = $(".dae")[0].innerText;
        model_url = model_url.replace(/^http:/, "https:");

        loader.load( model_url, function ( dae ) {
          object = dae.scene;
        }, onProgress, onError );
      });
    }
    else if ($(".obj").length > 0) {
      $.getScript("/js/lib/OBJLoader.js", function () {
        // Textures
        loadTextures();

        // Model
        var loader = new THREE.OBJLoader( manager );
        model_url = $(".obj")[0].innerText;
        model_url = model_url.replace(/^http:/, "https:");

        loader.load( model_url, function ( obj ) {
          object = obj;
        }, onProgress, onError );
      });
    }

    // Renderer
    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( viewW, viewH );
    viewer.append( renderer.domElement );

    // Camera Controls
    controls = new THREE.OrbitControls( camera, renderer.domElement );
    controls.screenSpacePanning = true;
    controls.minDistance = 10;
    controls.maxDistance = 10000;
    controls.target.set( 0, 2, 0 );
    controls.update();

    animate();
  }
});
