var viewer = OpenSeadragon({
    id: "openseadragon1",
    homeButton: "home",        
    zoomInButton: "zoom-in",
    zoomOutButton: "zoom-out",
    fullPageButton: "full-page",
    rotateRightButton: "right-rotate", 
    rotateLeftButton: "left-rotate", 

    //tileSources: srcs,
    crossOriginPolicy: 'Anonymous',
    collectionColumns: 6,
    collectionMode: true,
    showRotationControl: true
});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


var images = [];
for (var i = 0; i < items.length; i++) {
  viewer.addTiledImage({
      tileSource: 'https://dzis.nyc3.digitaloceanspaces.com/' + items[i][0] + '.dzi',
      success: function (event) {
        images.push(event.item);
      }
  });
}

addLinkOverlays()

async function addLinkOverlays() {
  // Wait until OSD is finished arranging the images so that the coordinates are accurate.
  await sleep (2000);
  for (var i = 0; images.length; i++) {
    addOneLinkOverlay(images[i], items[i][1], items[i][2]);
  }
}


function addOneLinkOverlay(image, link, name) {
    var imageRect = image.getBounds();
    var rect = new OpenSeadragon.Rect(imageRect.x, imageRect.y, 0.05, 0.05);
    console.log(rect);

    var divElement = document.createElement("div");
    var buttonElement = document.createElement("a");
    var imgElement = document.createElement("img");
    imgElement.src = '{% static 'edit_button.png' %}';
    imgElement.href = link;
    buttonElement.appendChild(imgElement);
    divElement.appendChild(buttonElement);

    var markElement = document.createElement("mark");
    var textElement = document.createTextNode(name);
    markElement.appendChild(textElement);
    divElement.appendChild(markElement);
    //buttonElement.className = "highlight";
    viewer.addOverlay(divElement, rect, OpenSeadragon.OverlayPlacement.CENTER);
 
    viewer.addViewerInputHook({
        hooks: [{
            tracker: "viewer",
            handler: "clickHandler",
            hookHandler: function (event) {
              event.preventDefaultAction = true;
              var pos = viewer.viewport.viewerElementToViewportCoordinates(event.position);
              if (isPointInsideRect(pos, rect.clone())) {
                  window.location.href = link;
              }
            },
        }]
    });
    viewer.viewport.goHome()
}


function isPointInsideRect(point, rect) {
    return point.x > rect.x && point.x < rect.x + rect.width && point.y > rect.y && point.y < rect.y + rect.height;
}
