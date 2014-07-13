#!/usr/bin/python
# alarma.py
# Detect movement using a PIR module with push notification using pushover service
#
# Authors : Ruben Garcia basen on sample script from Matt Hawkins
# Date    : 11/07/2014
# Push notifications with pushover: Ruben Garcia
# Date    : 22/04/2014
# Rev 1.2


# Import required Python libraries
import RPi.GPIO as GPIO
import time
from threading import Thread
from ConfigParser import SafeConfigParser

# Python 2.x compatible Doesnt works with 3.x
import httplib, urllib

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_PIR = 7

parser= SafeConfigParser()
parser.read ('/home/pi/alarm.ini')
url_pushover = parser.get('pushover_config','url')
app_key = parser.get('pushover_config','app_key')
user_key = parser.get('pushover_config','user_key')
cooldown_time = int(parser.get('pushover_config','cooldown_time'))
txt_finally = parser.get('localization','txt_finally')
txt_err_unknow = parser.get('localization','txt_err_unknow')
txt_disablealarm = parser.get('localization','txt_disablealarm')
txt_PIR_ready = parser.get('localization','txt_PIR_ready')
txt_PIR_tigered = parser.get('localization','txt_PIR_tigered')
txt_PIR_online = parser.get('localization','txt_PIR_online')
txt_PIR_waiting = parser.get('localization','txt_PIR_waiting')
txt_PUSH_err = parser.get('localization','txt_PUSH_err')
txt_PUSH_rearming = parser.get('localization','txt_PUSH_rearming')
txt_PUSH_ok = parser.get('localization','txt_PUSH_ok')
txt_PUSH_waitforserver = parser.get('localization','txt_PUSH_waitforserver')
txt_label = parser.get('localization','txt_label')

# Program name
print (txt_label)

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo

conn = httplib.HTTPSConnection(url_pushover)
# 0 ready, 1 sending
pushprocess = 0
# Send cooldown signal with 1
cooldown = 0
def threaded_PushAlarm():
    global conn, pushprocessfinish, cooldown, pushprocess    
    result=0   
    conn.request("POST", "/1/messages.json", urllib.urlencode({"token": app_key,"user": user_key,"message": "Movimiento Detectado",}), { "Content-type": "application/x-www-form-urlencoded" })
    result=conn.getresponse()        
    conn.close()
    print (txt_PUSH_waitforserver)
    while result==0:
	print (".")

    if result.status==200:
       	print (txt_PUSH_ok)
	print (txt_PUSH_rearming)
       	pushprocess=0
        cooldown=1
	# cooldown signal
    else:
	print (txt_PUSH_err)
	pushprocess=0

def MOTION(GPIO_PIR):
  global pushprocess
  # PIR is triggered
  print (txt_PIR_tigered)
  # Tiger push notification. Wait for the thread with pushprocess
  if pushprocess==0:
  	pushprocess=1
  	thread = Thread(target = threaded_PushAlarm)
  	thread.start()
  	thread.join()

try:
  GPIO.add_event_detect(GPIO_PIR, GPIO.RISING, callback=MOTION)
  while 1:
    # Wait for 10 milliseconds
    if cooldown==1:
	pushprocess=0
    	cooldown=0
	GPIO.remove_event_detect(GPIO_PIR)
	time.sleep(cooldown_time)
	GPIO.add_event_detect(GPIO_PIR, GPIO.RISING, callback=MOTION)
      
except KeyboardInterrupt:
  print (txt_disablealarm)
  # Reset GPIO settings
  # GPIO.cleanup()

except:
  print (txt_err_unknow)
  # Reset GPIO settings
  # GPIO.cleanup()

finally:
  # Reset GPIO settings
  print (txt_finally)  
  GPIO.cleanup()
