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
import random

# Scan device(must call one more time)
testOutPinsX = ControlGPIO.VGI_GPIO_PIN0 
testOutPins = testOutPinsX

testInPinsX = ControlGPIO.VGI_GPIO_PIN0
testInPins = testInPinsX

testPinOpenDrainX = ControlGPIO.VGI_GPIO_PIN0
testPinOpenDrain = testPinOpenDrainX


nRet = c_int(0)
nRet = ControlGPIO.VGI_ScanDevice(1)
if(nRet <= 0):
    print("No device connect!")
    exit()
else:
    print("Connected device number is:"+repr(nRet))

# Open device(must call)
nRet = ControlGPIO.VGI_OpenDevice(ControlGPIO.VGI_USBGPIO, 1, 0)
if(nRet != ControlGPIO.ERR_SUCCESS):
    print("Open device error!")
    exit()
else:
    print("Open device success!")


devIndex = c_int(1)

#! one before to read or write, remember to set all pins status 0
'''
print("****** start one ******")
nRet = ControlGPIO.VGI_SetOutput(ControlGPIO.VGI_USBGPIO, 1, 65535)
nRet = ControlGPIO.VGI_ResetPins(ControlGPIO.VGI_USBGPIO,1,65535)

nRet = ControlGPIO.VGI_SetPins(ControlGPIO.VGI_USBGPIO,1,0x001A)
'''

#! more
print("****** start more ******")
arr = [0x1A00, 0x2B00, 0x3C00, 0x4D00, 0x5E00, 0x6F00,0x7A00]
try:
    for testpins in arr:
        nRet = ControlGPIO.VGI_ResetPins(ControlGPIO.VGI_USBGPIO, devIndex, 65535-testpins)        
        nRet = ControlGPIO.VGI_SetPins(ControlGPIO.VGI_USBGPIO, devIndex, testpins)        
        sleep(2)

except KeyboardInterrupt:
    nRet = ControlGPIO.VGI_CloseDevice(ControlGPIO.VGI_USBGPIO, devIndex)
    if(nRet != ControlGPIO.ERR_SUCCESS):
        print("Close device error!")
        exit()
    else:
        print("Close device success!")

print("Toggle GPIO X output level end.")


# Close device
nRet = ControlGPIO.VGI_CloseDevice(ControlGPIO.VGI_USBGPIO, devIndex)
if(nRet != ControlGPIO.ERR_SUCCESS):
    print("Close device error!")
    exit()
else:
    print("Close device success!")
