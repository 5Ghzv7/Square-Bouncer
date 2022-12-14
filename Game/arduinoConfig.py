import serial
import serial.tools.list_ports as stlp
import time

class Ard:
    # Connects the Arduino
    def __init__(self) -> None:
        # Initializing variables
        self.arduino_connected = True
        self.arduino_data = []
        
        # Detecting Arduino
        arduino_ports = [
            p.device
            for p in stlp.comports()
            if "Arduino" in p.description
        ]
        if not arduino_ports:
            self.arduino_connected = False
        if len(arduino_ports) > 1:
            self.arduino_connected = True

        if self.arduino_connected:
            arduinoPort = arduino_ports[0]
            arduinoBR = 115200
            self.arduinoSerial = serial.Serial(arduinoPort, arduinoBR)
            print("Arduino connected!")
        else: print("Arduino NOT connected!")

    def getData(self) -> None:
        time.sleep(1)
        # Gets Information from "block_detection\detector.ino"
        while True:
            dataPacket = self.arduinoSerial.readline()
            dataPacket = str(dataPacket, "utf-8")
            dataPacket = dataPacket.strip("\r\n")
            try:
                if dataPacket != "#":
                    dataPacket = list(dataPacket.split("$$"))
                    dataPacket[0] = str(dataPacket[0])
                    dataPacket[1] = int(dataPacket[1])
                    self.arduino_data = dataPacket
                    print(f"Input -> lane: {self.arduino_data[0]}, plot: {self.arduino_data[1]}")
            except IndexError:
                print("Stopped receiving input!")
                break