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
password = 'password'

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
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
            buggy.beepHorn()
            buggy.motorOn("l","f",100)
            buggy.motorOn("r","f",100)
            sleep(0.5)
        elif request =='/lightoff?':
            pico_led.off()
            buggy.motorOff("r")
            buggy.motorOff("l")
            sleep(0.5)
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()

def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Motors on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Motors off" />
            </form>
            <p>Motor Status: {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)

buggy = KitronikPicoRobotBuggy()
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
