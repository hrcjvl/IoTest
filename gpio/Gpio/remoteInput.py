"""
Program test environment
Pyhone version:3.4.1
Firmware version:2.7.21
Dependent files(MacOSX):libGinkgo_Driver.dylib,libusb-0.1.4.dylib,libusb-1.0.0.dylib,ControlGPIO.py
Dependent files(Windows):Ginkgo_Driver.dll,ControlGPIO.py
Dependent files(Linux):libGinkgo_Driver.so,libusb-1.0.so,ControlGPIO.py
More Infomation:www.viewtool.com
"""

from ctypes import *
from time import sleep

# import USB-GPIO module
import ControlGPIO
import os

# Scan device(must call one more time)
testOutPinsX = ControlGPIO.VGI_GPIO_PIN0 
testOutPins = testOutPinsX

testInPinsX = ControlGPIO.VGI_GPIO_PIN0
testInPins = testInPinsX

testPinOpenDrainX = ControlGPIO.VGI_GPIO_PIN0
testPinOpenDrain = testPinOpenDrainX

i = c_ushort(0)
delay4input = c_ushort(0)

devIndex = c_int(1)
nRet = c_int(0)
nRet = ControlGPIO.VGI_ScanDevice(1)
if(nRet <= 0):
    print("No device connect!")
    exit()
else:
    print("Connected device number is:"+repr(nRet))

# Open device(must call)
nRet = ControlGPIO.VGI_OpenDevice(ControlGPIO.VGI_USBGPIO, devIndex, 0)
if(nRet != ControlGPIO.ERR_SUCCESS):
    print("Open device error!")
    exit()
else:
    print("Open device success!")


# set all pin status Input
testInPins = 65535
nRet = ControlGPIO.VGI_SetInput(ControlGPIO.VGI_USBGPIO, devIndex, testInPins)
if (nRet != ControlGPIO.ERR_SUCCESS):
    print("Set GPIO %x to input error!" %(testInPins))
    exit()
else:
    print("Set GPIO %x to input success!" %(testInPins))
print("Get GPIO X input level ...")
# Get GPIO X pin status
pin_value = c_ushort(0)
testInPins = 65535
while True:
    try:
        nRet = ControlGPIO.VGI_ReadDatas(ControlGPIO.VGI_USBGPIO, devIndex, testInPins,byref(pin_value))
        if nRet != ControlGPIO.ERR_SUCCESS:
            print("Pins data error")
            exit()
        else:
            sleep(0.5)
            hexstr = f"0x{pin_value.value:04x}"
            print(hexstr)

    except KeyboardInterrupt:
        nRet = ControlGPIO.VGI_CloseDevice(ControlGPIO.VGI_USBGPIO, devIndex)
        if(nRet != ControlGPIO.ERR_SUCCESS):
            print("Close device error!")
            exit()
        else:
            print("Close device success!")
        break

# Close device
nRet = ControlGPIO.VGI_CloseDevice(ControlGPIO.VGI_USBGPIO, devIndex)
if(nRet != ControlGPIO.ERR_SUCCESS):
    print("Close device error!")
    exit()
else:
    print("Close device success!")