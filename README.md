# The Eye of Sauron

An attempt to stop my dog from sleeping on my couch while I'm out of the
apartment.


## Background

My dog Angus realised that he can sleep on the couch when nobody's home to yell
at him. This program implements a very basic monitoring system that watches the
couch and yells at him if it detects him lying there.

![](http://i.imgur.com/tiqTTZK.jpg)


## Implementation

I've mounted a [webcam][webcam] on top of my TV, pointed it at the couch, and
plugged it into a [Raspberry Pi][pi]. The Pi runs this program, built with
Python 2.7 and [OpenCV][opencv].

So far I've only implemented basic motion detection:

![](http://i.imgur.com/XN89Tq8.gif)

Ultimately I plan to use the TV as an alarm system, triggering an unpleasantly
loud or high-pitched sound when Angus jumps onto the couch.


## References

 * http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/


 [webcam]: http://www.amazon.com/gp/product/B008ZVRAQS
 [pi]: https://www.raspberrypi.org/products/raspberry-pi-2-model-b/
 [opencv]: http://opencv.org/
