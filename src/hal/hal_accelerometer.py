import smbus
import time
import configparser
import math


CALIB_FILE = 'hal\accel_calib.txt'

class Regis(object):

    DEVID = 0x00
    THRESH_TAP = 0x1D
    OFSX = 0x1E
    OFSY = 0x1F
    OFSZ = 0x20
    DUR = 0x21
    Latent = 0x22
    Window = 0x23
    THRESH_ACT = 0x24
    THRESH_INACT = 0x25
    TIME_INACT = 0x26
    ACT_INACT_CTL = 0x27
    THRESH_FF = 0x28
    TIME_FF = 0x29
    TAP_AXES = 0x2A
    ACT_TAP_STATUS = 0x2B
    BW_RATE = 0x2C
    POWER_CTL = 0x2D
    INT_ENABLE = 0x2E
    INT_MAP = 0x2F
    INT_SOURCE = 0x30
    DATA_FORMAT = 0x31
    DATAX0 = 0x32
    DATAX1 = 0x33
    DATAY0 = 0x34
    DATAY1 = 0x35
    DATAZ0 = 0x36
    DATAZ1 = 0x37
    FIFO_CTL = 0x38
    FIFO_STATUS = 0x39


class DataRate(object):
    R_3200 = 0b1111
    R_1600 = 0b1110
    R_800 = 0b1101
    R_400 = 0b1100
    R_200 = 0b1011
    R_100 = 0b1010
    R_50 = 0b1001
    R_25 = 0b1000

class Range:
    G_2 = 0x00
    G_4 = 0x01
    G_8 = 0x02
    G_16 = 0x03

class ADXL345(object):
    def __init__(self, i2c_port=1, address=0x53):
        self.bus = smbus.SMBus(i2c_port)
        self.i2c_address = address
        self.scale_factor = 0.0039

        self.x = 0
        self.y = 0
        self.z = 0
        
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0

        self.x_gain = 1
        self.y_gain = 1
        self.z_gain = 1

    def set_data_rate(self, data_rate=DataRate.R_100):
        self.bus.write_byte_data(self.i2c_address, Regis.BW_RATE, data_rate)

    def set_range(self, g_range=Range.G_16, full_res=True):
        if full_res:
            data = g_range | 0x08
        else:
            data = g_range

        self.bus.write_byte_data(self.i2c_address, Regis.DATA_FORMAT, data)

    def clear_offset(self):
        self.bus.write_byte_data(self.i2c_address, Regis.OFSX, 0x00)
        self.bus.write_byte_data(self.i2c_address, Regis.OFSY, 0x00)
        self.bus.write_byte_data(self.i2c_address, Regis.OFSZ, 0x00)

    def measure_start(self):
        self.bus.write_byte_data(self.i2c_address, Regis.POWER_CTL, 0x08)

    def measure_stop(self):
        self.bus.write_byte_data(self.i2c_address, Regis.POWER_CTL, 0x00)

    def get_an_axis_raw(self, axis=Regis.DATAX0):
        byte_axis = self.bus.read_i2c_block_data(self.i2c_address, axis, 2)
        return self.convert_axis_data_raw(byte_axis[0], byte_axis[1])

    def get_3_axis_raw(self):
        byte_3_axis = self.bus.read_i2c_block_data(self.i2c_address, Regis.DATAX0, 6)
        x = self.convert_axis_data_raw(byte_3_axis[0], byte_3_axis[1])
        y = self.convert_axis_data_raw(byte_3_axis[2], byte_3_axis[3])
        z = self.convert_axis_data_raw(byte_3_axis[4], byte_3_axis[5])

        return x, y, z

    def get_an_axis(self, axis=Regis.DATAX0):
        byte_axis = self.bus.read_i2c_block_data(self.i2c_address, axis, 2)
        return self.convert_axis_data_raw(byte_axis[0], byte_axis[1])*self.scale_factor

    def get_3_axis(self):
        byte_3_axis = self.bus.read_i2c_block_data(self.i2c_address, Regis.DATAX0, 6)
        x = self.convert_axis_data_raw(byte_3_axis[0], byte_3_axis[1])*self.scale_factor
        y = self.convert_axis_data_raw(byte_3_axis[2], byte_3_axis[3])*self.scale_factor
        z = self.convert_axis_data_raw(byte_3_axis[4], byte_3_axis[5])*self.scale_factor

        return x, y, z
    
    def setTapDetection(self):
        self.bus.write_byte_data(self.i2c_address, 0x2A, 0xFF)
        
        self.bus.write_byte_data(self.i2c_address, 0x1D, 0x28)
        self.bus.write_byte_data(self.i2c_address, 0x21, 0x47)
        self.bus.write_byte_data(self.i2c_address, 0x2E, 0x60)
        self.bus.write_byte_data(self.i2c_address, 0x22, 0x40)
        self.bus.write_byte_data(self.i2c_address, 0x23, 0xF0)
        
    def getTapDetection(self):
        tap_byte = self.bus.read_byte_data(self.i2c_address, 0x30)
        self.bus.write_byte_data(self.i2c_address, 0x30, 0b00000000)
        if (bin(tap_byte)[3:5] == '10'):
            tap = 1
        if (bin(tap_byte)[3:5] == '11'):
            tap = 2
        if (bin(tap_byte)[3:5] == '00'):
            tap = 0
        return tap

    def get_an_axis_adjust(self, axis=Regis.DATAX0):
        byte_axis = self.bus.read_i2c_block_data(self.i2c_address, axis, 0)
        value = self.convert_axis_data_raw(byte_axis[0], byte_axis[1])

        if axis == Regis.DATAX0:
            value = (value - self.x_offset)/self.x_gain
        elif axis == Regis.DATAY0:
            value = (value - self.y_offset)/self.y_gain
        else:
            value = (value - self.z_offset)/self.z_gain

        return value

    def get_3_axis_adjusted(self):
        byte_3_axis = self.bus.read_i2c_block_data(self.i2c_address, Regis.DATAX0, 6)
        self.x = (self.convert_axis_data_raw(byte_3_axis[0], byte_3_axis[1]) - self.x_offset)/self.x_gain
        self.y = (self.convert_axis_data_raw(byte_3_axis[2], byte_3_axis[3]) - self.y_offset)/self.y_gain
        self.z = (self.convert_axis_data_raw(byte_3_axis[4], byte_3_axis[5]) - self.z_offset)/self.z_gain

        return self.x, self.y, self.z
        
    def get_pitch(self):
        return math.degrees(math.atan2(self.x, math.hypot(self.y, self.z)))

    def convert_axis_data_raw(self, lsb, msb):
        value = lsb | (msb << 8)

        if value & 0x8000:
            # 2's complement for negative data
            value = (-value ^ 0xFFFF) + 1

        return value

    def calibrate(self):
        calib_axis = {'+z': Regis.DATAZ0, '-z': Regis.DATAZ0,
                      '+y': Regis.DATAY0, '-y': Regis.DATAY0,
                      '+x': Regis.DATAX0, '-x': Regis.DATAX0
                      }
        axis_sequence = ['+z', '-z', '+y', '-y', '+x', '-x']
        collected_value = []
        avg_value = []

        self.clear_offset()
        self.measure_stop()
        self.measure_start()

        print("Calibration with data rate=100Hz, Please follow step by step")

        for axis in axis_sequence:
            print("******************************************")
            print("please put the sensor to ", axis, " axis")
            for i in range(5, -1, -1):
                time.sleep(1)
                print(axis, " will start in ", str(i))

            del collected_value[:]
            print("Collecting data for ", axis)
            for i in range(10):
                value = self.get_an_axis_raw(axis=calib_axis[axis])
                collected_value.append(value)
                time.sleep(0.1)

            avg_value.append(sum(collected_value)/len(collected_value))

        self.z_offset = int(round((avg_value[0] + avg_value[1])*0.5, 0))
        self.z_gain = int(round((avg_value[0] - avg_value[1])*0.5, 0))

        self.y_offset = int(round((avg_value[2] + avg_value[3]) * 0.5, 0))
        self.y_gain = int(round((avg_value[2] - avg_value[3]) * 0.5, 0))

        self.x_offset = int(round((avg_value[4] + avg_value[5]) * 0.5, 0))
        self.x_gain = int(round((avg_value[4] - avg_value[5]) * 0.5, 0))
        
        self.save_calib_value()

    def save_calib_value(self):
        config = configparser.ConfigParser()
        config['OFFSET'] = {'x_offset': str(self.x_offset),
                            'y_offset': str(self.y_offset),
                            'z_offset': str(self.z_offset)
                            }
        config['GAIN'] = {'x_gain': str(self.x_gain),
                          'y_gain': str(self.y_gain),
                          'z_gain': str(self.z_gain)
                          }
        with open(CALIB_FILE, 'w') as configfile:
            config.write(configfile)

    def load_calib_value(self):
        config = configparser.ConfigParser()
        config.read(CALIB_FILE)

        self.x_offset = int(config['OFFSET']['x_offset'])
        self.y_offset = int(config['OFFSET']['y_offset'])
        self.z_offset = int(config['OFFSET']['z_offset'])

        self.x_gain = int(config['GAIN']['x_gain'])
        self.y_gain = int(config['GAIN']['y_gain'])
        self.z_gain = int(config['GAIN']['z_gain'])


def init():
    ADDRESS=0x53

    acc=ADXL345(i2c_port=1,address=ADDRESS) #instantiate
    acc.load_calib_value() #load calib. values in accel_calib
    acc.set_data_rate(data_rate=DataRate.R_100) #see datasheet
    acc.set_range(g_range=Range.G_16,full_res=True) # ..
    acc.measure_start()

    return acc