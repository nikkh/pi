#!/usr/bin/python

import colorsys
from azure.servicebus import ServiceBusService
from azure.servicebus import Message
from blinkt import set_pixel, set_brightness, show, clear
import time
import json
class Payload(object):
     def __init__(self, j):
         self.__dict__ = json.loads(j)
def snake( r, g, b ):
    "This creates a snake effect on the blinkt using the specified colour"
    clear()
    for count in range(1,20):
        print(count)
        for i in range(8):
            clear()
            set_pixel(i, r, g, b)
            show()
            time.sleep(0.05)
    clear()
    return;

def rainbow():
	clear()
	spacing = 360.0 / 16.0
	hue = 0
	set_brightness(0.1)

	for count in range(1,160):
		print(count)
		hue = int(time.time() * 100) % 360
		for x in range(8):
			offset = x * spacing
			h = ((hue + offset) % 360) / 360.0
			r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
			set_pixel(x, r, g, b)
		show()
		time.sleep(0.001)
	return;

set_brightness(0.1) 
print('Nicks Raspberry Pi Python Service Bus Client version 0.1')
service_namespace='nixpitest'
key_name = 'RootManageSharedAccessKey' # SharedAccessKeyName from Azure portal
key_value = 'WaatrrP3nw+TMu2Qkw6vQQZrNca4ZS6kTOpOaxQt4Cc=' # SharedAccessKey from Azure portal
sbs = ServiceBusService(service_namespace,
                        shared_access_key_name=key_name,
                        shared_access_key_value=key_value)
sbs.create_queue('testpythonqueue1')
while True:
    newmsg = None
    newmsg = sbs.receive_queue_message('testpythonqueue1', peek_lock=False)
    print ("message: ", newmsg.body, "\n")
    if newmsg.body is not None:
        p = Payload(newmsg.body)
        if p.device: print(p.device)
        if p.effect: print(p.effect)
        if p.led: print(p.led)
        if p.colour: print(p.colour)
        if p.state: print(p.state)
        if p.effect == 'snake':
            if p.colour == 'red':
                snake(255,0,0)
            elif p.colour == 'green':
                snake(0,255,0)
            elif p.colour == 'blue':
                snake(0,0,255)
        if p.effect == 'rainbow':
            rainbow()
	clear()    
	time.sleep(1)

