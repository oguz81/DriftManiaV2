# DriftManiaV2
DriftMania is a 2D car drifting game developed with Python and Pygame module. 

NOTES
There are few problems in the game engine. First, the collision detection is not perfect because of pygame collision detection method. Pygame provides rectangles for the detection. However this rectangles can't be rotated around its centers and it causes ghost rectangles which crash the objects even they seem not to contact. The only solution -as far as i know- to fix it is to write the own collision detection function. 

The another point that doesn't satisfy the gamer is the drift engine. I think it works well in the long and wide turns but i'm not sure it's okay in small movements.

Hope you enjoy.
