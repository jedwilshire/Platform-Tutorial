# Platform-Tutorial Lesson 6
In this lesson we add world tiles using the tiled application
https://www.mapeditor.org/
The world.py module uses the pytmx module to process the world_01
tile map formed by tiled.
TILE_SIZE is removed from settings because we no longer should use it.
Platforms are now drawn to a world image and the Platform
class will no longer assign an image as the Platform's rect is 
actually invisible.
the draw_grid method is removed from debugging options in main
as it no longer is usefull.  Instead debugging shows the
outlines of platforms through a method calld draw_platform_outlines