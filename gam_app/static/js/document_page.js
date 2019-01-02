var viewer = OpenSeadragon({
    id: "openseadragon1",
    homeButton: "home",
    zoomInButton: "zoom-in",
    zoomOutButton: "zoom-out",
    fullPageButton: "full-page",
    rotateRightButton: "right-rotate",
    rotateLeftButton: "left-rotate",

    tileSources: srcs,
    crossOriginPolicy: 'Anonymous',
    collectionColumns: 6,
    collectionMode: true,
    showRotationControl: true
});


