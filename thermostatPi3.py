from guizero import *
import sys
from PIL import Image
import socket
import struct
import time
import datetime
import ntplib
from time import ctime

# Setting up the main App window properies
app = App(title="thermostatPi3", layout="grid", height=600, width=800)
app.tk.attributes("-fullscreen",True)

# Material design dark theme settings.
app.bg = "#121212"
app.text_color = "white"


def GetNTPDateTime(server):
    try:
        ntpDate = None
        client = ntplib.NTPClient()
        response = client.request(server, version=3)
        response.offset
        ntpDate = ctime(response.tx_time)
        #print (ntpDate)
    except Exception as e:
        print (e)
    return datetime.datetime.strptime(ntpDate, "%a %b %d %H:%M:%S %Y")


def do_nothing():
    print("A picture button was pressed")
    on_off.image = "resources/shut-down-line(1).png"
    sys.exit(0)


###
wifi_logo = Picture(app, image="resources/wifi-line.png", grid=[0,0], align="top")

thermostatPi3_name = Text(app, text="          thermostatPi3          ", grid=[1, 0], align="top")

on_off = PushButton(app, image="resources/shut-down-line(1).png", command=do_nothing, grid=[2, 0],  align="left")

###
calendar_logo = Picture(app, image="resources/calendar-event-fill.png", grid=[0, 1], align="top")

temp_up = Picture(app, image="resources/arrow-up-s-fill.png", grid=[2, 1], align="top")

###

mode = Picture(app, image="resources/robot-line.png", grid=[0, 2], align="top")

temperature = Text(app, text="      18 C              ", grid=[1, 2], align="top")

set_temp = Text(app, text="      23 C ", grid=[2,2], align="top")


###
temp_down = Picture(app, image="resources/arrow-down-s-fill.png", grid=[2,3], align="top")

###
date = Text(app, text="Lunedi 23 Gennaio ", grid=[0,4], align="top")
print(GetNTPDateTime('0.de.pool.ntp.org')) 
#date.set(GetNTPDateTime('0.de.pool.ntp.org'))

heat_on_off = Picture(app, image="resources/fire-fill.png", grid=[1,4], align="top")
hour = Text(app, text="     22:33    ", grid=[2,4], align="top")
app.display()
