from guizero import *
import sys
from PIL import Image

app = App(title="thermostatPi3", layout="grid", height=600, width=800)


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
heat_on_off = Picture(app, image="resources/fire-fill.png", grid=[1,4], align="top")
hour = Text(app, text="     22:33    ", grid=[2,4], align="top")
app.display()
