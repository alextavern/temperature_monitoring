""" a simple script that reads data from arduino uno using pyserial """

from typing import Union
import threading
import serial
import time

PORT = "/dev/ttyACM0"
BAUD = 9600


class ArduinoTemperatureSensors:

    def __init__(self, port: str, baud: int) -> None:
        """creates the arduino object and opens the serial port"""

        self._port = serial.Serial()
        self._port.port = port
        self._port.baudrate = baud

        self._thread = threading.Thread(target=self.read)
        self._thread.start()
        self._running = True
        self._temperatures_are_set = threading.Event()

        self.temperatures = {}

    def read(self) -> None:
        """reads, decodes and saves the datastream into a dict"""

        with self._port as port:
            while True:
                if port.in_waiting:
                    packet_bytes = port.readline()
                    packet_string = packet_bytes.decode("utf").strip()

                    temperatures = packet_string.split("|")
                    timestamp = time.time()
                    self.temperatures = {i: float(temp) for i, temp in enumerate(temperatures) if temp}
                    self.temperatures["timestamp"] = timestamp
                    self._temperatures_are_set.set()

                if not self._running:
                    break

    def get(self, sensor: int=None) -> Union[dict, int]: 
        self._temperatures_are_set.wait()
        return self.temperatures[sensor] if sensor is not None else self.temperatures

    def stop(self) -> None:
        self._running = False
        self._thread.join()
        self.temperatures = {}

    def __del__(self) -> None:
        self.stop()


if __name__ == "__main__":

    temperature_data = []
    sensors = ArduinoTemperatureSensors(PORT, BAUD)

    for i in range(3840):
        temps = sensors.get()
        with open("20241110_temperature_over_we.txt", "a") as f:
            f.write(f"{temps}\n")
        time.sleep(60)