from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from phue import Bridge
from colorpy import colormodels
import os

dispatcher = SoapDispatcher(
    'hue',
    location="http://localhost:8080/",
    namespace="http://www.sonos.com/Services/1.1",
    trace=True,
    debug=True)


def getSessionId(username, password):
    print "getSessionId(%s, %s) called" % (username, password)
    return username

dispatcher.register_function('getSessionId', getSessionId,
                             returns={'getSessionIdResult': str},
                             args={'username': str, 'password': str})

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


def getMetadata(id, index, count):
    print "getMetadata(%s, %s, %s) called" % (id, index, count)
    response = {}
    if id == 'root':  # root
        response = {'getMetadataResult': [
            {'index': 0, 'count': 2, 'total': 2},
            {'mediaCollection': {'id': 'light1', 'title': 'Bedroom', 'itemType': 'container', 'canPlay': False}},
            {'mediaCollection': {'id': 'light2', 'title': 'Living Room', 'itemType': 'container', 'canPlay': False}}
        ]}
    elif id == "light1":
        response = {'getMetadataResult': [
            {'index': 0, 'count': 8, 'total': 8},
            {'mediaMetadata': {'id': 'light1_blue', 'title': 'Blue', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                               'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}},
            {'mediaMetadata': {'id': 'light1_red', 'title': 'Red', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                               'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}},
            {'mediaMetadata': {'id': 'light1_green', 'title': 'Green', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                               'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}},
            {'mediaMetadata': {'id': 'light1_white', 'title': 'White', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                               'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}},
            {'mediaMetadata': {'id': 'light1_off', 'title': 'Off', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                               'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}},
            {'mediaMetadata': {'id': 'light1_slowon', 'title': 'Slow On', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                               'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}},
            {'mediaMetadata': {'id': 'light1_slowoff', 'title': 'Slow Off', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                               'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}},
            {'mediaMetadata': {'id': 'light1_dim', 'title': 'Dim', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                               'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
        ]}
    return response

dispatcher.register_function('getMetadata', getMetadata,
                             returns={'getMetadataResult': {
                                 'index': int,
                                 'count': int,
                                 'total': int,
                                 'mediaCollection': mediaCollection}},
                             args={'id': str, 'index': int, 'count': int})


def getMediaMetadata(id):
    print "getMediaMetadata(%s) called" % id
    response = {}
    if id == "light1_blue":
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'light1_blue', 'title': 'Blue', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                                      'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
    elif id == "light1_red":
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'light1_red', 'title': 'Red', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                                      'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
    elif id == "light1_green":
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'light1_green', 'title': 'Green', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                                      'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
    elif id == "light1_white":
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'light1_white', 'title': 'White', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                                      'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
    elif id == "light1_off":
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'light1_off', 'title': 'Off', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                                                                'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
    elif id == "light1_slowon":
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'light1_slowon', 'title': 'Slow On', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                                                                'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
    elif id == "light1_slowoff":
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'light1_slowoff', 'title': 'Slow Off', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                                                                'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
    elif id == "light1_dim":
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'light1_dim', 'title': 'Dim', 'mimeType': 'audio/mpeg', 'itemType': 'track',
                                                                'trackMetadata': {'artist': 'Bedroom', 'albumArtist': 'Bedroom', 'genreId': 'Bedroom', 'duration': 1}}}
    else:
        response['getMediaMetadataResult'] = {'mediaMetadata': {'id': 'ERROR', 'title': 'ERROR', 'mimeType': 'ERROR', 'itemType': 'track',
                                      'trackMetadata': {'artist': 'ERROR', 'albumArtist': 'ERROR', 'genreId': 'ERROR', 'duration': 1}}}
        print "No MediaMetadata found for id = %s" % id
    return response

dispatcher.register_function('getMediaMetadata', getMediaMetadata,
                             returns={'getMediaMetadataResult': mediaMetadata},
                             args={'id': str})


def getMediaURI(id):
    print "getMediaURI(%s) called" % id
    response = {'getMediaURIResult': 'http://192.168.1.164:8080/hue/' + id}
    return response

dispatcher.register_function('getMediaURI', getMediaURI,
                             returns={'getMediaURIResult': str},
                             args={'id': str})


def getLastUpdate():
    print "getLastUpdate() called"
    response = {'getLastUpdateResult': {'catalog': '0', 'favorites': '0', 'pollInterval': 60}}
    return response

dispatcher.register_function('getLastUpdate', getLastUpdate,
                             returns={'getLastUpdateResult': {
                                 'catalog': str,
                                 'favorites': str,
                                 'pollinterval': int}},
                             args=None)


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
        print "do_GET() called with path %s" % self.path
        if self.path.endswith("light1_blue"):
            bridge.set_light(2, {'on': True, 'bri': 254, 'xy': rgb(0, 0, 255)})
        elif self.path.endswith("light1_red"):
            bridge.set_light(2, {'on': True, 'bri': 254, 'xy': rgb(255, 0, 0)})
        elif self.path.endswith("light1_green"):
            bridge.set_light(2, {'on': True, 'bri': 254, 'xy': rgb(0, 255, 0)})
        elif self.path.endswith("light1_white"):
            bridge.set_light(2, {'on': True, 'bri': 254, 'xy': rgb(255, 255, 255)})
        elif self.path.endswith("light1_off"):
            bridge.set_light(2, {'on': False})
        elif self.path.endswith("light1_slowon"):
            bridge.set_light(2, {'transitiontime': 150, 'on': True, 'bri': 254})
        elif self.path.endswith("light1_slowoff"):
            bridge.set_light(2, {'transitiontime': 150, 'on': True, 'bri': 0})
        elif self.path.endswith("light1_dim"):
            bridge.set_light(2, {'on': True, 'bri': 127})

    # Without this override, BaseHTTPServer performs a reverse DNS lookup to print out the connecting client.
    # This takes like five seconds per request! Ain't nobody got time for that!
    def address_string(self):
        host, port = self.client_address[:2]
        #return socket.getfqdn(host)
        return host

print "Connecting to Hue server..."
bridge = Bridge("192.168.1.140")
bridge.connect()
print "Starting SMAPI server..."
httpd = HTTPServer(("", 8080), HueSOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()