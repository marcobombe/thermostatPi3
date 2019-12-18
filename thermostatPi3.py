from guizero import *
import time
import datetime
from datetime import datetime
import sys
# Setting up the main App window properies
app = App(title="thermostatPi3", layout="grid", height=600, width=800)
#app.tk.attributes("-fullscreen",True)

# Material design dark theme settings.
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
    current_time.value = get_time()
    
# Current date update function    
def update_date():
    current_date.value = get_date()

def do_nothing():
    print("A picture button was pressed")
    on_off.image = "resources/shut-down-line(1).png"
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
        connection_status.image = "resources/wifi-line.png"
    else:
        connection_status.image = "resources/wifi-off-line.png"
   
# Setting up the main graphic
        
# Setup the connection status indication        
connection_status = Picture(app, image="resources/wifi-line.png", grid=[0,0], align="left")
connection_status.repeat(20000, update_connection_status)

# Setup the App name
thermostatPi3_name = Text(app, text="          thermostatPi3          ", grid=[1, 0], align="top")

# Temperature controls
temp_up = PushButton(app, image="resources/arrow-drop-up-line.png", grid=[2, 1], align="right")
temp_down = PushButton(app, image="resources/arrow-drop-down-line.png", grid=[2,3], align="right")


on_off = PushButton(app, image="resources/shut-down-line(1).png", command=do_nothing, grid=[2, 0],  align="left")

###
calendar_logo = Picture(app, image="resources/calendar-event-fill.png", grid=[0, 1], align="top")



###

mode = Picture(app, image="resources/robot-line.png", grid=[0, 2], align="top")

temperature = Text(app, text="      18 C              ", grid=[1, 2], align="top")

set_temp = Text(app, text="      23 C ", grid=[2,2], align="top")


###


###


heat_on_off = Picture(app, image="resources/fire-fill.png", grid=[1,4], align="top")

# Show system date and update it every second
current_date = Text(app, text=get_date(), grid=[0,4], align="left")
current_date.repeat(5000, update_date) 

# Show system time and update it every second
current_time = Text(app, text= get_time(), grid=[2,4], align="right")
current_time.repeat(3000, update_time)

# Final App display
app.display()
