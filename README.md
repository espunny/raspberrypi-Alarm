raspberrypi-Alarm v1.02beta
------------------------
Author: Rubén García
based on the original PIR module script of Matt Hawkins

A simple Alarm script written in python for the raspberrypi and a PIR sensor using push notifications over Pushover.net

NOTICE!!!!!!!!!!!!
This script has been writed for "Wheezy Raspbian" distribution and actually only works with python 2.7.x.
For Python 3, httplib has been replaced with http.client and urlencode has moved to urllib.parse.
!!!!!!!!!!!!!!!!!!!

Use
Connect the PIR sensor to the Raspberry:
http://www.raspberrypi-spy.co.uk/2013/01/cheap-pir-sensors-and-the-raspberry-pi-part-1/

Edit the alarm.ini file, by default the cooldown_time is defined on: 1200 seconds.
Ensure that the "app_key" and the "user_key" are assigned correctly.

run the alarm: sudo python alarma.py
Close the alarm with Ctrl+C

How Works
--------------------------------------------------------------------------------------
When a movement is detected a thread is launched to contact with the Pushover server. If the alarm message is sent, the PIR sensor waits a number of seconds (defined in cooldown_time) until is ready again.
If the network or the pushover web service fails, the alarm try again with the next movement.

Programming the alarm
---------------------
You can program and disable the push notifications by your pushover app.

Future implementations
----------------------
-Play a sound file on a thread.
-Use of the Raspberry pi 5Mpx original camera to send a number photos by email or ftp account.
