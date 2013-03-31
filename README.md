# sonoshue: Sonos Hue Server

## Introduction

The product of an "innovation week" at Sonos, this Python program performs three functions:
* Interfaces with a Phillips Hue hub by using [studioimaginaire's phue script](https://github.com/studioimaginaire/phue)
* Provides an interface for this for a Sonos system via a SMAPI service
* By interpreting specific "play" commands received from a Sonos ZonePlayer, provides control over the Phillips Hue bulbs.

## Benefits

* You don't have to use the (kind of awful) Phillips Hue app
* Setting alarms to turn on a light is a fair bit easier
* Build a playlist where the light changes from song to song!
* Build a playlist comprised exclusively of light controls, put it on loop and shuffle, and you've got yourself a disco!

## Requirements

* [colorpy](http://markkness.net/colorpy/ColorPy.html), to convert RGB to the Hue's XY format (thanks [isaackelly](https://github.com/issackelly/python-hue))
* [pysimplesoap](https://code.google.com/p/pysimplesoap/), as all communication with your Sonos components is via SOAP

##License

WTFPL - http://www.wtfpl.net

<a href="http://www.wtfpl.net/"><img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png" width="80" height="15" alt="WTFPL" /></a>
