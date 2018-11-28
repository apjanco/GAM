function myFunction() {
    window.open(
        PERSONA_UPDATE_URL,
        "_blank",
        "location=yes,height=800,width=800,scrollbars=yes,status=yes"
    );
}


function myFunctionLugar() {
    window.open(
        LUGAR_UPDATE_URL,
        "_blank",
        "location=yes,height=800,width=800,scrollbars=yes,status=yes"
    );
}


function myFunctionOrganizacion() {
    window.open(
        ORGANIZACION_URL,
        "_blank",
        "location=yes,height=800,width=800,scrollbars=yes,status=yes"
    );
}


var viewer = OpenSeadragon({
    id: "openseadragon1",
    homeButton: "home",
    zoomInButton: "zoom-in",
    zoomOutButton: "zoom-out",
    fullPageButton: "full-page",
    rotateRightButton: "right-rotate",
    rotateLeftButton: "left-rotate",

    tileSources: SRCS,
    crossOriginPolicy: 'Anonymous',
    collectionColumns: 6,
    collectionMode: true,
    showRotationControl: true
});


viewer.world.addHandler("add-item", function (event) {
    var tiledImage = event.item;
    tiledImage.addHandler("fully-loaded-change", function() {
        // Wait until the images are fully loaded to add the link overlays.
        if (areAllFullyLoaded()) {
            var count = viewer.world.getItemCount();
            for (var i = 0; i < count; i++) {
                var tiledImage = viewer.world.getItemAt(i);
                addLinkOverlay(tiledImage, ITEMS[i][1], ITEMS[i][2]);
            }
        }
    });
});


function areAllFullyLoaded() {
    var count = viewer.world.getItemCount();
    for (var i = 0; i < count; i++) {
        var tiledImage = viewer.world.getItemAt(i);
        if (!tiledImage.getFullyLoaded()) {
            return false;
        }
    }
    return true;
}


function addLinkOverlay(image, link, name) {
    var imageRect = image.getBounds();
    var rect = new OpenSeadragon.Rect(imageRect.x, imageRect.y, 0.05, 0.05);

    var divElement = document.createElement("div");
    var buttonElement = document.createElement("a");
    var imgElement = document.createElement("img");
    imgElement.src = EDIT_BUTTON_URL;
    imgElement.href = link;
    buttonElement.appendChild(imgElement);
    divElement.appendChild(buttonElement);

    var markElement = document.createElement("mark");
    var textElement = document.createTextNode(name);
    markElement.appendChild(textElement);
    divElement.appendChild(markElement);
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
    return (
        point.x > rect.x && point.x < rect.x + rect.width 
        && point.y > rect.y && point.y < rect.y + rect.height
    );
}
