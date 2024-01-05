from time import sleep
import argparse
import smbus

ADDRESS = 0x44

COMMAND_MEAS_HIGHREP = 0x2C
COMMAND_RESULT = 0x00


class SHT31(object):
    def __init__(self, address=ADDRESS):
        self._address = address
        self._bus = smbus.SMBus(1)

    def get_temperature_humidity(self):
        self.write_list(COMMAND_MEAS_HIGHREP, [0x06])
        sleep(0.1)

        data = self.read_list(COMMAND_RESULT, 6)
        temperature = -45 + (175 * (data[0] * 256 + data[1]) / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        return temperature, humidity

    def read_list(self, register, length):
        return self._bus.read_i2c_block_data(self._address, register, length)

    def write_list(self, register, data):
        self._bus.write_i2c_block_data(self._address, register, data)
