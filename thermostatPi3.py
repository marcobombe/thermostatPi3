from guizero import *
import time
import datetime
from datetime import datetime
import sys

from thermo_configuration import init_db
from thermo_configuration import read_conf
from thermo_configuration import read_conf_param
from thermo_configuration import write_conf_param

# Global Variables

current_temp = 0.0
set_point_temp = 0.0
mode = "AUTO"

auto_str = "AUTO"
man_str = "MAN"

heat = "OFF"

temp_udm = " °C"

# Setting up the main App window properies
app = App(title="thermostatPi3", layout="grid")
# app.tk.attributes("-fullscreen",True)

init_db()
read_conf()
read_conf_param('thermostatPi', 'config_version')
print(read_conf_param('thermostatPi', 'config_version'))
print(read_conf_param('global_settings', 'hysteresis'))

# Material design dark theme settings_w.
app.bg = "#121212"
app.text_color = "white"


# Get the current Date
def get_date():
    now = datetime.now()
    system_date = now.strftime("%b-%d-%Y")
    return system_date


# Get the current Time
def get_time():
    now = datetime.now()
    system_time = now.strftime("%H:%M")
    return system_time


# Current time update function
def update_time():
    current_time_w.value = get_time()


# Current date update function    
def update_date():
    current_date_w.value = get_date()


def do_nothing():
    print("A picture button was pressed")
    # on_off_w.image = "resources/shut-down-line.png"
    time.sleep(1)
    sys.exit(0)


# Verify the internet connection  
try:
    import httplib
except:
    import http.client as httplib


def internet_connection_check():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


# Connection status update function    
def update_connection_status():
    if internet_connection_check():
        # connection_status_w.image = "resources/wifi-line.png"
        connection_status_w.value = "WIFI-ON"
        connection_status_w.text_color = "green"
    else:
        # connection_status_w.image = "resources/wifi-off-line.png"
        connection_status_w.value = "WIFI-OFF"
        connection_status_w.text_color = "red"


# Set Point Management
def increase_set_point():
    global set_point_temp
    global mode
    set_point_temp = set_point_temp + 1
    mode = "MAN"


def decrease_set_point():
    global set_point_temp
    global mode
    set_point_temp = set_point_temp - 1
    mode = "MAN"


def update_setpoint_indication():
    global set_point_temp
    set_point_indication_w.value = str(set_point_temp) + temp_udm


def update_mode_indication():
    global mode
    mode_w.value = mode
    if mode == "AUTO":
        mode_w.text_color = "green"
    else:
        mode_w.text_color = "yellow"


def update_heat_status():
    global heat
    heat_on_off_w.value = "HEAT " + heat


def settings_window_open():
    settings_window.show(wait=True)


def settings_window_close():
    settings_window.hide()


def settings_apply():
    write_conf_param("global_settings", "hysteresis", str(hysteresis_slider.value))


# Setting up the main graphic

# Setup the connection status indication        
# connection_status_w = Picture(app, image="resources/wifi-line.png", grid=[0,0], align="left")
connection_status_w = Text(app, text="WIFI", grid=[0, 0], align="left")
connection_status_w.repeat(8000, update_connection_status)

# Setup the App name
thermostatPi3_name_w = Text(app, text="       thermostatPi3", grid=[1, 0], align="left")
thermostatPi3_name_w.text_color = "gray"

# Temperature controls
# temp_up_w = PushButton(app, image="resources/arrow-drop-up-line.png", grid=[2, 1], align="right")
# temp_down_w = PushButton(app, image="resources/arrow-drop-down-line.png", grid=[2,3], align="right")
temp_up_w = PushButton(app, text="TEMP UP", command=increase_set_point, grid=[2, 1], align="right")
temp_up_w.tk.config(highlightthickness=0)
temp_up_w.tk.config(borderwidth=0)
temp_up_w.text_color = "red"

temp_down_w = PushButton(app, text="TEMP DOWN", command=decrease_set_point, grid=[2, 3], align="right")
temp_down_w.tk.config(highlightthickness=0)
temp_down_w.tk.config(borderwidth=0)
temp_down_w.text_color = "blue"

# Settings
settings_w = PushButton(app, text="Settings", command=settings_window_open, grid=[0, 3], align="left")
settings_w.tk.config(highlightthickness=0)
settings_w.tk.config(borderwidth=0)

# On-Off control (debug only)
# on_off_w = PushButton(app, image="resources/shut-down-line.png", command=do_nothing, grid=[2, 0],  align="left")
on_off_w = PushButton(app, text="OFF", command=do_nothing, grid=[2, 0], align="right")
on_off_w.tk.config(highlightthickness=0)
on_off_w.tk.config(borderwidth=0)
on_off_w.text_color = "red"

# Calendar function
# calendar_logo_w = Picture(app, image="resources/calendar-event-fill.png", grid=[0, 1], align="left")
calendar_logo_w = Text(app, text="CALENDAR", grid=[0, 1], align="top")

# Mode Indication
# mode_w = Picture(app, image="resources/robot-line.png", grid=[0, 2], align="top")
mode_w = Text(app, text="AUTO", grid=[0, 2], align="left")
mode_w.repeat(100, update_mode_indication)

# Current Temperature Indication
temperature_indication_w = Text(app, text="       0.0" + temp_udm, grid=[1, 2], align="left")

# Set Point Indication
set_point_indication_w = Text(app, text="       0.0" + temp_udm, grid=[2, 2], align="right")
set_point_indication_w.repeat(100, update_setpoint_indication)

# Heat on-off Indication
# heat_on_off_w = Picture(app, image="resources/fire-fill.png", grid=[1,4], align="top")
heat_on_off_w = Text(app, text="       HEAT OFF", grid=[1, 4], align="left")
heat_on_off_w.repeat(100, update_heat_status)

# Show system date and update it every second
current_date_w = Text(app, text=get_date(), grid=[0, 4], align="left")
current_date_w.repeat(5000, update_date)

# Show system time and update it every second
current_time_w = Text(app, text=get_time(), grid=[2, 4], align="right")
current_time_w.repeat(3000, update_time)

update_connection_status()

settings_window = Window(app, title="Settings", layout="grid")
# settings_window.tk.attributes("-fullscreen",True)

# Material design dark theme settings_w.
settings_window.bg = "#121212"
settings_window.text_color = "white"

settings_title = Text(settings_window, "Settings: ", grid=[0, 0])
hysteresis = Text(settings_window, "  hysteresis: ", grid=[0, 1])
# hysteresis_setting_value = TextBox(settings_window, text="15", grid=[1,1])
# hysteresis_setting_value.tk.config(highlightthickness = 0)
# hysteresis_setting_value.tk.config(borderwidth=0)

# def hysteresis_slider_changed(hysteresis_slider):
#    hysteresis_setting_value.value = hysteresis_slider

hysteresis_slider = Slider(settings_window, start=5, end=60, grid=[2, 1])
# hysteresis_slider.value = 15
hysteresis_slider.value = int(read_conf_param('global_settings', 'hysteresis'))
hysteresis_slider.tk.config(highlightthickness=0)
hysteresis_slider.tk.config(borderwidth=0)

min_label = Text(settings_window, "minutes.", grid=[3, 1])

apply = PushButton(settings_window, text="Apply", command=settings_apply, grid=[3, 4])
apply.tk.config(highlightthickness=0)
apply.tk.config(borderwidth=0)
apply.text_color = "yellow"

close = PushButton(settings_window, text="Close", command=settings_window_close, grid=[4, 4])
close.tk.config(highlightthickness=0)
close.tk.config(borderwidth=0)
close.text_color = "red"

settings_window.hide()

# Final App display
app.display()
