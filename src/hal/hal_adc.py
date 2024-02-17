import spidev #import SPI library
from time import sleep


def init():
    global spi
    spi=spidev.SpiDev() #create SPI object
    spi.open(0,0) #open SPI port 0, device (CS) 0

def get_adc_value(adcnum):
    #read SPI data from the MCP3008, 8 channels in total
    if adcnum>7 or adcnum<0:
        return -1
    spi.max_speed_hz = 1350000
    r=spi.xfer2([1,8+adcnum<<4,0])
        #construct list of 3 items, before sending to ADC:
        #1(start), (single-ended+channel#) shifted left 4 bits, 0(stop)
        #see MCP3008 datasheet for details
    data=((r[1]&3)<<8)+r[2]
        #ADD first byte with 3 or 0b00000011 - masking operation
        #shift result left by 8 bits
        #OR result with second byte, to get 10-bit ADC result
    return data

