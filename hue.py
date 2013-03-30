from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from phue import Bridge
from colorpy import colormodels
import os
import sys
import socket

dispatcher = SoapDispatcher(
    'hue',
    location="http://localhost:8080/",
    namespace="http://www.sonos.com/Services/1.1",
    trace=True,
    debug=True)


# Converts RGB inputs to an xy. From https://github.com/issackelly/python-hue
def rgb(red, green=None, blue=None):
    if isinstance(red, basestring):
        # assume a hex string is passed
        rstring = red
        red = int(rstring[1:3], 16)
        green = int(rstring[3:5], 16)
        blue = int(rstring[5:], 16)

    # We need to convert the RGB value to Yxy.
    colormodels.init(phosphor_red=colormodels.xyz_color(0.64843, 0.33086), phosphor_green=colormodels.xyz_color(0.4091,0.518), phosphor_blue=colormodels.xyz_color(0.167, 0.04))
    xyz = colormodels.irgb_color(red, green, blue)
    xyz = colormodels.xyz_from_rgb(xyz)
    xyz = colormodels.xyz_normalize(xyz)

    return [xyz[0], xyz[1]]

lightActions = {'on': {'on': True},
                'off': {'on': False},
                'dim': {'on': True, 'bri': 127},
                'red': {'on': True, 'bri': 254, 'xy': rgb(255, 0, 0)},
                'green': {'on': True, 'bri': 254, 'xy': rgb(0, 255, 0)},
                'blue': {'on': True, 'bri': 254, 'xy': rgb(0, 0, 255)},
                'white': {'on': True, 'bri': 254, 'xy': rgb(255, 255, 255)},
                'slow_on': {'transitiontime': 300, 'on': True, 'bri': 254},
                'slow_off': {'transitiontime': 300, 'on': True, 'bri': 0}
                }

mediaCollection = {'id': str,
                   'title': str,
                   'itemType': str,
                   'artistId': str,
                   'artist': str,
                   'albumArtURI': str,
                   'canPlay': bool,
                   'canEnumerate': bool,
                   'canAddToFavorites': bool,
                   'canScroll': bool,
                   'canSkip': bool}

trackMetadata = {'artist': str,
                 'albumArtist': str,
                 'genreId': str,
                 'duration': int}

mediaMetadata = {'id': str,
                 'title': str,
                 'mimeType': str,
                 'itemType': str,
                 'trackMetadata': trackMetadata}


def getSessionId(username, password):
    print "getSessionId(%s, %s) called" % (username, password)
    return username

dispatcher.register_function('getSessionId', getSessionId,
                             returns={'getSessionIdResult': str},
                             args={'username': str, 'password': str})


def getMetadata(id, index, count):
    print "getMetadata(%s, %s, %s) called" % (id, index, count)
    response = {}
    if id == 'root':  # root
        lights = bridge.get_light_objects('list')
        response = {'getMetadataResult': [
            {'index': 0, 'count': len(lights), 'total': len(lights)}]}
        for light in lights:
            response['getMetadataResult'].append({'mediaCollection': {'id': str(light.light_id),
                                                                      'title': light.name,
                                                                      'itemType': 'container',
                                                                      'canPlay': False}})
    else:
        response = {'getMetadataResult': [{'index': 0, 'count': len(lightActions), 'total': len(lightActions)}]}
        print "getting light"
        light = bridge.lights[int(id)]
        print "got light"
        for action in lightActions:
            response['getMetadataResult'].append({'mediaMetadata': {'id': id + '/' + action,
                                                                    'title': action.title(),
                                                                    'mimeType': 'audio/mpeg',
                                                                    'itemType': 'track',
                                                                    'trackMetadata': {'artist': light.name,
                                                                                      'albumArtist': light.name,
                                                                                      'genreId': light.name,
                                                                                      'duration': 1}}})
    print "response: %s" % response
    return response

dispatcher.register_function('getMetadata', getMetadata,
                             returns={'getMetadataResult': {
                                 'index': int,
                                 'count': int,
                                 'total': int,
                                 'mediaCollection': mediaCollection}},
                             args={'id': str, 'index': int, 'count': int})


def getMediaMetadata(id):
    room = id.split('/')[0]
    command = id.split('/')[1]
    print "getMediaMetadata(%s) called with room %s and command %s" % (id, room, command)
    response = {'getMediaMetadataResult': {'mediaMetadata': {'id': id,
                                                             'title': command.title(),
                                                             'mimeType': 'audio/mpeg',
                                                             'itemType': 'track',
                                                             'trackMetadata': {'artist': room,
                                                                               'albumArtist': room,
                                                                               'genreId': room,
                                                                               'duration': 1}}}}
    return response

dispatcher.register_function('getMediaMetadata', getMediaMetadata,
                             returns={'getMediaMetadataResult': mediaMetadata},
                             args={'id': str})


def getMediaURI(id):
    print "getMediaURI(%s) called" % id
    response = {'getMediaURIResult': 'http://' + localIP + ':8080/hue/' + id}
    print 'pointed ZP to http://' + localIP + ':8080/hue/' + id
    return response

dispatcher.register_function('getMediaURI', getMediaURI,
                             returns={'getMediaURIResult': str},
                             args={'id': str})


# This gets called every once in a while so I created a function that does nothing but respond to it.
# I think it's so the Controller can cache music when nothing has changed.
def getLastUpdate():
    print "getLastUpdate() called"
    response = {'getLastUpdateResult': {'catalog': '0', 'favorites': '0', 'pollInterval': 60}}
    return response

dispatcher.register_function('getLastUpdate', getLastUpdate,
                             returns={'getLastUpdateResult': {
                                 'catalog': str,
                                 'favorites': str,
                                 'pollInterval': int}},
                             args=None)


class HueSOAPHandler(SOAPHandler):

    # Receives a play request, returns a one second silent MP3, and based on the URL changes the light colour.
    def do_GET(self):
        f = open("1sec.mp3", 'rb')
        st = os.fstat(f.fileno())
        self.send_response(200)
        self.send_header("Content-type", "audio/mpeg")
        self.send_header("Content-Length", st.st_size)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        light = self.path.split("/")[-2]
        command = self.path.split("/")[-1]
        if command.endswith('favicon.ico'):
            return  # to reduce errors when trying to access light commands via browser
        print "do_GET() called with light %s and command %s = %s" % (light, command, lightActions[command])
        bridge.set_light(light, lightActions[command])

    # Without this override, BaseHTTPServer performs a reverse DNS lookup to print out the connecting client.
    # This takes like five seconds per request! Ain't nobody got time for that!
    def address_string(self):
        host, port = self.client_address[:2]
        #return socket.getfqdn(host)
        return host

if len(sys.argv) < 2:
    print "Sonos Hue Server, by Malcolm Crum"
    print "Usage: python hue.py <huehubIP>"
else:
    hueIP = sys.argv[1]
    print "Connecting to Hue server at %s..." % hueIP
    bridge = Bridge(hueIP)
    bridge.connect()

    # Figure out your IP address. Mildly complex because you may have multiple interfaces on your machine.
    # So, we find the IP of the interface that has the hub on it, and hope that your Sonos system is on the same
    # one.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hueIP, 80))
    localIP = sock.getsockname()[0]
    sock.close()
    print "Detected local IP %s" % localIP

    print "Starting SMAPI server..."
    httpd = HTTPServer(("", 8080), HueSOAPHandler)
    httpd.dispatcher = dispatcher
    httpd.serve_forever()