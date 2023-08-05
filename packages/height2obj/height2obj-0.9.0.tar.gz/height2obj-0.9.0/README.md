# hight2obj

Converts a heightmap to a 3d mesh.

**Usage**

hight2obj SOURCE DESTINATION SCALE

**Parameters**

* SOURCE: Filename of the source hightmap. This must be a 8 bpp greyscale bitmap-type image. PNG is tested an recommended.
* DESTINATION: Filename of the destination file into which the 3d data is written.
* SCALE: Scale factor for the z-coordinate. This value is the maximum height of the resulting mesh relative to the short side side of the SOURCE image.

**Remarks**

This script uses the pillow library to load the image. Output format Wavefront OBJ.

This only creates a 3d surface, no solid block.

Make shure to install this package via pip to allow comfortable use in console.
