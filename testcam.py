'''testcam.py
load and display a ONVIF cam image using pygame and io
'''
import io
import pygame as pg
from urllib.request import urlopen

_stream_header = "Content-Length: "
# Get a JPEG Image from the video stream
def _get_stream_jpeg():
    image = None
 
    while True:
        restart = False
        # skip the observed header
        for item in _stream_header:
            data = _connection.read(1)
            print(data.decode("utf-8"))
            if not data.decode("utf-8") == item:
                restart = True
                break
 
        # if the header failed retry processing
        if restart:
            continue
 
        print('done')
        # get the length of the jpeg
        str_jpeg_length = ""
        while True:
            item = _connection.read(1)
            if item.decode("utf-8") == "\r":
                break
            else:
                str_jpeg_length += item.decode("utf-8")
 
        # skip the last line LF and the next line CR LF combo (len('\r+\n+\r') = 3)
        item = _connection.read(3)
 
        # now cast string to int
        jpeg_length = 0
        try:
            jpeg_length = int(str_jpeg_length)
        except ValueError:
            jpeg_length = 0
 
        # if zero this is bad so return None
        if jpeg_length == 0:
            return image
 
        print(jpeg_length)
        #else read the image
        image = _connection.read(jpeg_length)
        print('done')
        # skip the ending CR LF so the buffer is ready for a new jpeg reply
        item = _connection.read(2)
 
        return image



# initialize pygame
pg.init()
# on a webpage right click on the image you want and use Copy image URL

image_url = "http://209.137.241.162:8080/mjpg/video.mjpg"
_connection = urlopen(image_url)
#text = _connection.read(80)
#print(text)
#g.quit()
#exit(0)

image = _get_stream_jpeg()
# create a file object (stream)
image_file = io.BytesIO(image)
# (r, g, b) color tuple, values 0 to 255
white = (255, 255, 255)
# create a 600x400 white screen
screen = pg.display.set_mode([0,0], pg.FULLSCREEN)
screen.fill(white)
# load the image from a file or stream
image = pg.image.load(image_file)
# draw image, position the image ulc at x=20, y=20
screen.blit(image, (0, 0))
# nothing gets displayed until one updates the screen
pg.display.flip()
# start event loop and wait until
# the user clicks on the window corner x to exit
done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
           if event.key == pg.K_ESCAPE or event.unicode == 'q':
              done = True
pg.quit()
exit(0)