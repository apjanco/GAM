



var duomo = {
  Image: {
    xmlns: "http://schemas.microsoft.com/deepzoom/2008",
    Url: "//openseadragon.github.io/example-images/duomo/duomo_files/",
    Format: "jpg",
    Overlap: "2",
    TileSize: "256",
    Size: {
      Width:  "13920",
      Height: "10200"
    }
  }
};

var test = [duomo, duomo,duomo];


var viewer = OpenSeadragon({
  id: "seadragon-viewer",
  prefixUrl: "//openseadragon.github.io/openseadragon/images/",
  tileSources: SRC,
  collectionMode:       true,
  collectionRows:       2,
  collectionTileSize:   1024,
  collectionTileMargin: 100,
});

