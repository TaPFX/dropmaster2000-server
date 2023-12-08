#OSC server um eine NEtzwerk Schnittstelle fuer den Dropmaster2000 zu ermoeglichen

import argparse
import math
import socket
import time

import RPi.GPIO as GPIO

from pythonosc import dispatcher
from pythonosc import osc_server

drop4Pin = 2
drop3Pin = 3
drop2Pin = 4
drop1Pin = 14
statusLED = 17

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(drop1Pin, GPIO.OUT)
GPIO.setup(drop2Pin, GPIO.OUT)
GPIO.setup(drop3Pin, GPIO.OUT)
GPIO.setup(drop4Pin, GPIO.OUT)

GPIO.output(drop1Pin, GPIO.HIGH)
GPIO.output(drop2Pin, GPIO.HIGH)
GPIO.output(drop3Pin, GPIO.HIGH)
GPIO.output(drop4Pin, GPIO.HIGH)

GPIO.setup(statusLED, GPIO.OUT)
GPIO.output(statusLED, GPIO.LOW)

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 while True:
  try:
   if s.connect(("8.8.8.8",80)) == None:
    ip_address = s.getsockname()[0]
    s.close()
    break
  except:
   print("try again")
  finally:
   s.close()
     
 return ip_address

def drop_handler(address, *args):
  print(f"{address}: {args}")
  if address == "/drop/1":
    print("drop 1")
    GPIO.output(drop1Pin, GPIO.LOW)
  elif address == "/drop/2":
    print("drop 2")
    GPIO.output(drop2Pin, GPIO.LOW)
  elif address == "/drop/3":
    print("drop 3")
    GPIO.output(drop3Pin, GPIO.LOW)
  elif address == "/drop/4":
    print("drop 4")
    GPIO.output(drop4Pin, GPIO.LOW) 
  else:
    print("Ungueltiger Kanal")
    
  GPIO.output(statusLED, GPIO.LOW)
  
  time.sleep(1)
  
  GPIO.output(drop1Pin, GPIO.HIGH)
  GPIO.output(drop2Pin, GPIO.HIGH)
  GPIO.output(drop3Pin, GPIO.HIGH)
  GPIO.output(drop4Pin, GPIO.HIGH)
  GPIO.output(statusLED, GPIO.HIGH)
  #Set Drop Pins to ON for 1 sec

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

if __name__ == "__main__":
  local_ip = get_ip_address()
  print(local_ip)
  
  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/drop/*", drop_handler)
  dispatcher.set_default_handler(default_handler)

  server = osc_server.ThreadingOSCUDPServer((local_ip, 50005), dispatcher)
  print("Serving on {}".format(server.server_address))

  GPIO.output(statusLED, GPIO.HIGH)

  server.serve_forever()
