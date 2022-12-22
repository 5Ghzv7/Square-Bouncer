import serial
import serial.tools.list_ports as stlp

class Ard:
    # Connects the Arduino
    def __init__(self) -> None:
        # Initializing variables
        self.arduino_connected = True
        self.arduino_data_none = True
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
        else:
            print("Arduino NOT connected!")

    def getData(self) -> bool:
        # Gets Information from "block_detection\detector.ino"
        while True:
            dataPacket = self.arduinoSerial.readline()
            dataPacket = str(dataPacket, "utf-8")
            dataPacket = str(dataPacket.strip("\r\n"))
            if dataPacket != "#":
                dataPacket = list(dataPacket.split("$$"))
                dataPacket[0] = str(dataPacket[0])
                dataPacket[1] = int(dataPacket[1])
                dataPacket[2] = float(dataPacket[2])
                self.arduino_data = dataPacket
                self.arduino_data_none = False
            else: self.arduino_data_none = True