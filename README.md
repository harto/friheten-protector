# Friheten-Protector

An attempt to stop my dog from sleeping on my [couch][friheten] while I'm out of
the apartment.


## Background

My dog Angus realised that he can sleep on the couch when nobody's home to yell
at him. I intend to implement a monitoring system that _will_ yell at him if it
detects him on the couch.


## Implementation

**Disclaimer: I have no idea if the following is technically feasible.**

I intent to point a webcam at the couch and plug it into a [Raspberry Pi][pi].
The Pi will run a program, built with [OpenCV][opencv], that detects movement
through the camera.

When movement is detected, an unpleasantly loud alarm will sound. (This might
be achieved by plugging the Pi into my TV.) My hope is that this will frighten
Angus into getting off the couch.



 [friheten]: http://www.ikea.com/us/en/catalog/products/70243038/#/50242997
 [pi]: https://www.raspberrypi.org/products/raspberry-pi-2-model-b/
 [opencv]: http://opencv.org/
