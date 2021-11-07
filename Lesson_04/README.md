# Platform-Tutorial Lesson 4
In this lesson, we create a camera class to allow for longer platform levels.
We create a camera that uses what we call a Camera_Portal object.
The camera portal object creates a rectangle that allows movement of the player within
without moving the camera perspective.  When the player moves on the outside of
the portal it will move with the player.
|-------------------------------|
|                               |
|                               |
|        |--------|             |
|        |        |             |
|________|_____P__|_____________|