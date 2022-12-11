import warnings
import time
import serial
import serial.tools.list_ports

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if "Arduino" in p.description
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn("Multiple Arduinos found - using the first")

arduinoData = serial.Serial(arduino_ports[0], 9600)

time.sleep(5)

while True:
    while arduinoData.inWaiting() == 0:
        pass
    dataPacket = arduinoData.readline()
    dataPacket = str(dataPacket, "utf-8")
    dataPacket.strip("\r\n")

    splitPacket = dataPacket.split(",")

    x = int(splitPacket[0])
    y = int(splitPacket[1])
    z = int(splitPacket[2])
    print(f"x = {x}, y = {y}, z = {z}")