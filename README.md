# python-ray-tracer
A simple ray-tracing program written in python

This project was my first time using python for anything that requried more than 10 lines of code. As a result, the code is pretty awful. I have no intention of improving the project from its current state, even though I've learned enough to fix some of its biggest issues.

How to use:
I've included a few sample "Scene_*.py" files. These files just contain data such as number of objects, position of objects, what type of material the objects use, etc. Simply running a Scene file will produce an image after a few minutes. Before creating new scene files, here is one important thing to know:
Image dimensions have to be square and specific sizes. I've found 500x500px to be optimal. 1000x1000 also works. I attempted to add support for different image sizes, but I failed miserably, and most other image sizes will prouce really screwed-up images. The code for the camera class is embarrasingly awful. Any image size over 1000x1000 will probably use over a gigabyte of RAM. Oh well. I have no intention of changing it.
