# sonoshue: Sonos Hue Server

## Introduction

The product of the Q1 2013 Innovation Week at Sonos, this Python program performs three functions:
* Interfaces with a Phillips Hue hub by using [studioimaginaire's phue script](https://github.com/studioimaginaire/phue)
* Provides an interface for this for a Sonos system via a SMAPI service
* By interpreting specific "play" commands received from a Sonos ZonePlayer, provides control over the Phillips Hue bulbs.

## Benefits

* You don't have to use the (kind of awful) Phillips Hue app
* Setting alarms to turn on a light is a fair bit easier
* Build a playlist where the light changes from song to song!
* Build a playlist comprised exclusively of light controls, put it on loop and shuffle, and you've got yourself a disco!

## Usage

* Press the button on your Hue hub (only necessary the first time)
* python hue.py <hueHubIP>
* In a web browser, access http://<ZonePlayerIP>:1400/customsd.htm
** Enter "Hue" as the name
** Change SID if you have added other custom services to your Sonos system
** Both endpoints are http://<yourIP>:8080/hue
** Login: Anonymous
** Leave other settings as-is
* On your Sonos system, access the Service Settings menu, and add Hue
* Control your Hue lights from the new Hue entry on your Music Menu

## Requirements

* [pysimplesoap](https://code.google.com/p/pysimplesoap/), as all communication with your Sonos components is via SOAP

##License

WTFPL - http://www.wtfpl.net

<a href="http://www.wtfpl.net/"><img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png" width="80" height="15" alt="WTFPL" /></a>
