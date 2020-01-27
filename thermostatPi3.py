# Guizero import
from guizero import *

# System related imports
import sys
import os

# Time and date related imports
import time
import datetime
from datetime import datetime
import calendar

# Program logging system related imports
import logging

# Permanent configuration utility imports
from thermo_configuration import init_conf
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


# Main functions

# Update current logging system logging 
def update_log_level(selected_value):
    logger = logging.getLogger()
    if selected_value == "DEBUG":
        logger.setLevel(logging.DEBUG)
        logging.critical('Logging level now is DEBUG')
    elif selected_value == "INFO":
        logger.setLevel(logging.INFO)
        logging.critical('Logging level now is INFO')
    elif selected_value == "WARNING":
        logger.setLevel(logging.WARNING)
        logging.critical('Logging level now is WARNING')
    elif selected_value == "ERROR":
        logger.setLevel(logging.ERROR)
        logging.critical('Logging level now is ERROR')
    elif selected_value == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
        logging.critical('Logging level now is CRITICAL')


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


def program_quit():
    logging.critical('ThermostatPi3 quitted by user.')
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
        connection_status_w.value = "WIFI-ON"
        connection_status_w.text_color = "green"
    else:
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


def calendar_window_open():
    calendar_window.show(wait=True)


def calendar_window_close():
    calendar_window.hide()


def settings_apply():
    write_conf_param("global_settings", "hysteresis", str(hysteresis_slider.value))
    logger = logging.getLogger()

    if logger.getEffectiveLevel() == 50:
        write_conf_param("others", "logging_level", "CRITICAL")
        logger.setLevel(logging.CRITICAL)
    elif logger.getEffectiveLevel() == 40:
        write_conf_param("others", "logging_level", "ERROR")
        logger.setLevel(logging.ERROR)
    elif logger.getEffectiveLevel() == 30:
        write_conf_param("others", "logging_level", "WARNING")
        logger.setLevel(logging.WARNING)
    elif logger.getEffectiveLevel() == 20:
        write_conf_param("others", "logging_level", "INFO")
        logger.setLevel(logging.INFO)
    elif logger.getEffectiveLevel() == 10:
        write_conf_param("others", "logging_level", "DEBUG")
        logger.setLevel(logging.DEBUG)
    elif logger.getEffectiveLevel() == 0:
        write_conf_param("others", "logging_level", "NOTSET")
        logger.setLevel(logging.NOTSET)


def clear_log():
    if os.path.exists("thermo_log.log"):
        f = open('thermo_log.log', 'r+')
        f.truncate(0)
        logging.critical('User clear the log.')
    else:
        logging.critical('Log file does not exist.')


# Setting up the main App window properies
app = App(title="thermostatPi3", layout="grid")
# app.tk.attributes("-fullscreen",True)

# Setting up the logging system
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    handlers=[
        logging.FileHandler("thermo_log.log"),  # TODO: settings option for the optional use of RotatingFileHandler
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()
logging.info('ThermostatPi started')
logging.info('Logging started')

# Permanent configuration startup test, and initialization
init_conf()

# Basic configuration file chech
read_conf()
read_conf_param('thermostatPi', 'config_version')

# Update logging level
update_log_level(read_conf_param("others", "logging_level"))

# Material design dark theme settings_w.
app.bg = "#121212"
app.text_color = "white"

# Setting up the main graphic

# Setup the connection status indication        
connection_status_w = Text(app, text="WIFI", grid=[0, 0], align="left")
connection_status_w.repeat(8000, update_connection_status)

# Setup the App name
thermostatPi3_name_w = Text(app, text="       thermostatPi3", grid=[1, 0], align="left")
thermostatPi3_name_w.text_color = "gray"

# Temperature controls
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
on_off_w = PushButton(app, text="OFF", command=program_quit, grid=[2, 0], align="right")
on_off_w.tk.config(highlightthickness=0)
on_off_w.tk.config(borderwidth=0)
on_off_w.text_color = "red"

# Calendar function
# calendar_logo_w = Text(app, text="CALENDAR", grid=[0, 1], align="top")
calendar_w = PushButton(app, text="CALENDAR", command=calendar_window_open, grid=[0, 1], align="left")
calendar_w.tk.config(highlightthickness=0)
calendar_w.tk.config(borderwidth=0)

# Mode Indication
mode_w = Text(app, text="AUTO", grid=[0, 2], align="left")
mode_w.repeat(100, update_mode_indication)

# Current Temperature Indication
temperature_indication_w = Text(app, text="       0.0" + temp_udm, grid=[1, 2], align="left")

# Set Point Indication
set_point_indication_w = Text(app, text="       0.0" + temp_udm, grid=[2, 2], align="right")
set_point_indication_w.repeat(100, update_setpoint_indication)

# Heat on-off Indication
heat_on_off_w = Text(app, text="       HEAT OFF", grid=[1, 4], align="left")
heat_on_off_w.repeat(100, update_heat_status)

# Show system date and update it every second
current_date_w = Text(app, text=get_date(), grid=[0, 4], align="left")
current_date_w.repeat(5000, update_date)

# Show system time and update it every second
current_time_w = Text(app, text=get_time(), grid=[2, 4], align="right")
current_time_w.repeat(3000, update_time)

update_connection_status()

# Settings Window
settings_window = Window(app, title="Settings", layout="grid")
# settings_window.tk.attributes("-fullscreen",True)

# Material design dark theme for settings window.
settings_window.bg = "#121212"
settings_window.text_color = "white"

settings_title = Text(settings_window, "Settings: ", grid=[0, 0], align="left")
hysteresis = Text(settings_window, "Hysteresis: ", grid=[0, 1], align="left")

hysteresis_slider = Slider(settings_window, start=5, end=60, grid=[1, 1], align="left")
hysteresis_slider.value = int(read_conf_param('global_settings', 'hysteresis'))
hysteresis_slider.tk.config(highlightthickness=0)
hysteresis_slider.tk.config(borderwidth=0)

minutes_label = Text(settings_window, "minutes.", grid=[2, 1], align="left")

log_label = Text(settings_window, "Logging level: ", grid=[0, 4], align="left")

combo = Combo(settings_window, options=["", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], command=update_log_level,
              grid=[1, 4], align="left")
combo.value = read_conf_param('others', 'logging_level')

clear_log = PushButton(settings_window, text="Clear Log", command=clear_log, grid=[2, 4])
clear_log.tk.config(highlightthickness=0)
clear_log.tk.config(borderwidth=0)
clear_log.text_color = "red"

apply = PushButton(settings_window, text="Apply", command=settings_apply, grid=[2, 5])
apply.tk.config(highlightthickness=0)
apply.tk.config(borderwidth=0)
apply.text_color = "yellow"

close = PushButton(settings_window, text="Close", command=settings_window_close, grid=[3, 5])
close.tk.config(highlightthickness=0)
close.tk.config(borderwidth=0)
close.text_color = "red"

settings_window.hide()

# Calendar Window
calendar_window = Window(app, title="Calendar", layout="grid")
# calendar_window.tk.attributes("-fullscreen",True)

# Material design dark theme for settings window.
calendar_window.bg = "#121212"
calendar_window.text_color = "white"

calendar_title = Text(calendar_window, "Calendar: ", grid=[0, 0], align="left")

i = 1
for day in calendar.day_name:
    # print (day[0:3])
    Text(calendar_window, day[0:3], grid=[0, i], align="left")
    i = i + 1
    hours = range(0, 23)
    for count in hours:
        count = count + 1
        PushButton(calendar_window, text=str(count) + ":00", grid=[count, i])

calendar_window.hide()

# Final App display
app.display()
