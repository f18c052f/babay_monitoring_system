from time import sleep
import smbus

ADDRESS = 0x44
COMMAND_MEAS_HIGHREP = 0x2C
COMMAND_RESULT = 0x00
DELAY_AFTER_COMMAND = 0.1


class SHT31(object):
    _address = ADDRESS
    _bus = smbus.SMBus(1)

    @classmethod
    def get_temperature_humidity(cls) -> (float, float):
        cls._write_list(COMMAND_MEAS_HIGHREP, [0x06])
        sleep(DELAY_AFTER_COMMAND)

        data = cls._read_list(COMMAND_RESULT, 6)
        temperature = -45 + (175 * (data[0] * 256 + data[1]) / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        return temperature, humidity

    @classmethod
    def _read_list(cls, register: int, length: int):
        try:
            return cls._bus.read_i2c_block_data(cls._address, register, length)
        except IOError as e:
            print(f"SHT31 Read Data Error: {e}")

    @classmethod
    def _write_list(cls, register: int, data):
        try:
            cls._bus.write_i2c_block_data(cls._address, register, data)
        except IOError as e:
            print(f"SHT31 Write Data Error: {e}")
