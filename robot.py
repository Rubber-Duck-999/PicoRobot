from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep
from machine import Timer 
import network
dir(network)
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

ssid = 'IpHoster'
password = ''

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 6000)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def serve(connection):
    #Start a web server
    state = False
    pico_led.off()
    brightness = 50
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        stringdata = request.decode('utf-8')
        print('Message: {}, {}'.format(stringdata, len(stringdata)))
        if 'on' in stringdata:
            pico_led.on()
            state = True
            buggy.beepHorn()
            buggy.setLED(0, buggy.RED)
            buggy.setLED(1, buggy.GREEN)
            buggy.setLED(2, buggy.BLUE)
            buggy.setLED(3, buggy.PURPLE)
            buggy.setBrightness(brightness)
            buggy.show()
            client.send('Understood')
        elif 'off' in stringdata:
            pico_led.off()
            buggy.beepHorn()
            sleep(3)
            buggy.setLED(0, buggy.RED)
            buggy.setLED(1, buggy.GREEN)
            buggy.setLED(2, buggy.BLUE)
            buggy.setLED(3, buggy.PURPLE)
            buggy.setBrightness(0)
            buggy.show()
            state = False
            client.send('Understood')
        elif 'forward' in stringdata and state:
            buggy.motorOn("l","f",30)
            buggy.motorOn("r","f",30)
            sleep(1)
            buggy.motorOff("r")
            buggy.motorOff("l")
        elif 'backward' in stringdata and state:
            buggy.motorOn("l","r",30)
            buggy.motorOn("r","r",30)
            sleep(1)
            buggy.motorOff("r")
            buggy.motorOff("l")
        else:
            client.send('Could not understand the message')
        client.close()

buggy = KitronikPicoRobotBuggy()
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
