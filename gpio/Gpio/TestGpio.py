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

# Scan device(must call one more time)
testOutPinsX = ControlGPIO.VGI_GPIO_PIN0 
testOutPins = testOutPinsX

testInPinsX = ControlGPIO.VGI_GPIO_PIN0
testInPins = testInPinsX

testPinOpenDrainX = ControlGPIO.VGI_GPIO_PIN0
testPinOpenDrain = testPinOpenDrainX

i = c_ushort(0)
delay4input = c_ushort(0)

nRet = c_int(0)
nRet = ControlGPIO.VGI_ScanDevice(1)
if(nRet <= 0):
    print("No device connect!")
    exit()
else:
    print("Connected device number is:"+repr(nRet))

# Open device(must call)
nRet = ControlGPIO.VGI_OpenDevice(ControlGPIO.VGI_USBGPIO, 0, 0)
if(nRet != ControlGPIO.ERR_SUCCESS):
    print("Open device error!")
    exit()
else:
    print("Open device success!")

# Set GPIO X to output
# print("Config GPIO X to output ...")
# for i in range(16):
#     testOutPins = 1<<i
#     if(testOutPins == (1<<3)):
#         testOutPins=1<<5
#     if(testOutPins == (1<<4)):
#         testOutPins=1<<5
        
#     nRet = ControlGPIO.VGI_SetOutput(ControlGPIO.VGI_USBGPIO, 0, testOutPins)
#     if(nRet != ControlGPIO.ERR_SUCCESS):
#         print("Set GPIO %x to output error!" %(testOutPins))
#         exit()
#     else:
# #        print("Set GPIO_7 and GPIO_8 to output success!")
#          print("Set GPIO %x to output success!" %(testOutPins))

# print("Config GPIO X to output end.")

print("Toggle GPIO X output level ...")
pin_value = c_ushort(0)
for i in range(16):
    testOutPins = 1<<i    
    if(testOutPins == (1<<3)):
        testOutPins=1<<5
    if(testOutPins == (1<<4)):
        testOutPins=1<<5
        
    # Set GPIO_X to high
    nRet = ControlGPIO.VGI_SetPins(ControlGPIO.VGI_USBGPIO, 0, testOutPins);
    if (nRet != ControlGPIO.ERR_SUCCESS):
    #    print("Set pin low error!")
        print ("Set pin %x high error!" %(testOutPins))
        exit()
    else:
    #    print("Set pin low success!")
        print ("Set pin %x high success!" %(testOutPins))
    sleep(0.2)
    # Set GPIO_X to low
    nRet = ControlGPIO.VGI_ResetPins(ControlGPIO.VGI_USBGPIO, 0, testOutPins);
    if (nRet != ControlGPIO.ERR_SUCCESS):
    #    print("Set pin low error!")
        print ("Set pin %x low error!" %(testOutPins))
        exit()
    else:
    #    print("Set pin low success!")
        print ("Set pin %x low success!" %(testOutPins))

    sleep(0.2)
print("Toggle GPIO X output level end.")


# Set GPIO_X to low
#nRet = ControlGPIO.VGI_ResetPins(ControlGPIO.VGI_USBGPIO, 0, testOutPins);
#if (nRet != ControlGPIO.ERR_SUCCESS):
#    print("Set GPIO_7 and GPIO_8 low error!")
#    exit()
#else:
#    print("Set GPIO_7 and GPIO_8 low success!")
#
## Put delay here
#sleep(0.5)
#
## Set GPIO_7 and GPIO_8 to high
#nRet = ControlGPIO.VGI_SetPins(ControlGPIO.VGI_USBGPIO, 0, testOutPins);
#if (nRet != ControlGPIO.ERR_SUCCESS):
#    print("Set GPIO_7 and GPIO_8 high error!")
#    exit()
#else:
#    print("Set GPIO_7 and GPIO_8 high success!")

# Put delay here
#sleep(1)

print("Set GPIO X to input ...")
# Set GPIO X to input
for i in range(16):
    testInPins = 1<<i
    if(testInPins == (1<<3)):
        testInPins=1<<5
    if(testInPins == (1<<4)):
        testInPins=1<<5
        
    nRet = ControlGPIO.VGI_SetInput(ControlGPIO.VGI_USBGPIO, 0, testInPins);
    if (nRet != ControlGPIO.ERR_SUCCESS):
        print("Set GPIO %x to input error!" %(testInPins))
        exit()
    else:
        print("Set GPIO %x to input success!" %(testInPins))

print("Set GPIO X to input end.")

print("Get GPIO X input level ...")
nRet = ControlGPIO.VGI_SetInput(ControlGPIO.VGI_USBGPIO, 0, 0xFFFF);
if (nRet != ControlGPIO.ERR_SUCCESS):
    print("Set GPIO %x to input error!" %(testInPins))
    exit()
else:
    print("Set GPIO %x to input success!" %(testInPins))
# Get GPIO X pin status
pin_value = c_ushort(0)
for delay4input in range(20):
    print("delay4input: %d ." %(delay4input))
    for i in range(16):
        testInPins = 1<<i
        if(testInPins == (1<<3)):
            testInPins=(1<<5)
        if(testInPins == (1<<4)):
            testInPins=(1<<5)
            
        nRet = ControlGPIO.VGI_ReadDatas(ControlGPIO.VGI_USBGPIO, 0, testInPins, byref(pin_value))
        if (nRet != ControlGPIO.ERR_SUCCESS):
            print("Get pin data error!")
            exit()
        else:
            sleep(0.5)
            if ((pin_value.value & testInPins) != 0):
                print("GPIO: %x is high-level!"%(testInPins))
            else:
                print("GPIO: %x is low-level!"%(testInPins))

print("Get GPIO X input level end.")

# ======== Get GPIO_X pins status end ==========

print("Set GPIO X open drain ...")
# Set GPIO X pins to opendrain
# for i in range(16):
#     testPinOpenDrain = 1<<i
#     if(testPinOpenDrain == (1<<3)):
#         testPinOpenDrain=1<<5
#     if(testPinOpenDrain == (1<<4)):
#         testPinOpenDrain=1<<5
        
#     nRet = ControlGPIO.VGI_SetOpenDrain(ControlGPIO.VGI_USBGPIO, 0, testPinOpenDrain)
#     if(nRet != ControlGPIO.ERR_SUCCESS):
#         print("Set GPIO X to OpenDrain error!" %(testPinOpenDrain))
#         exit()
#     else:
#         print("Set GPIO X to OpenDrain success!" %(testPinOpenDrain))

# print("Test GPIO X opendrain end ")


# Close device
nRet = ControlGPIO.VGI_CloseDevice(ControlGPIO.VGI_USBGPIO, 0)
if(nRet != ControlGPIO.ERR_SUCCESS):
    print("Close device error!")
    exit()
else:
    print("Close device success!")
