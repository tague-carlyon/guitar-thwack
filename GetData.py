""" 
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-03-08

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import time
import sys
import matplotlib.pyplot as plt
import numpy


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

Num_Samples = 16384
hdwf = c_int()
sts = c_byte()
rgdSamples1 = (c_double*Num_Samples)()
rgdSamples2 = (c_double*Num_Samples)()
Total = numpy.zeros(Num_Samples)
N_run = 30
Sample_Rate = 40000.0


version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
# 2nd configuration for Analog Discovery with 16k analog-in buffer
#dwf.FDwfDeviceConfigOpen(c_int(-1), c_int(1), byref(hdwf)) 

if hdwf.value == hdwfNone.value:
    szError = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szError);
    print("failed to open device\n"+str(szError.value))
    quit()

##print("Generating square wave...")
###                                    AWG 1     carrier
##dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(0), c_int(1))
##dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), c_int(0), funcSquare)
##dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), c_int(0), c_double(11))
##dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), c_int(0), c_double(1.0))
##dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), c_int(0), c_double(1.0))
##dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1))

#set up acquisition
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(Sample_Rate))
dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(Num_Samples)) 
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0))
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1))
#dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(1), c_double(5))

#set up trigger
dwf.FDwfAnalogInTriggerAutoTimeoutSet(hdwf, c_double(0)) #disable auto trigger
dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcDetectorAnalogIn) #one of the analog in channels
#dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcExternal1)

dwf.FDwfAnalogInTriggerTypeSet(hdwf, trigtypeEdge)
dwf.FDwfAnalogInTriggerChannelSet(hdwf, c_int(0)) # first channel
dwf.FDwfAnalogInTriggerLevelSet(hdwf, c_double(0.5)) # 0.5V
#dwf.FDwfAnalogInTriggerConditionSet(hdwf, DwfTriggerSlopeEither) 
dwf.FDwfAnalogInTriggerConditionSet(hdwf, DwfTriggerSlopeRise) 

#or use trigger from other instruments or external trigger
#dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcExternal1) 
#dwf.FDwfAnalogInTriggerConditionSet(hdwf, DwfTriggerSlopeEither) 

# wait at least 2 seconds with Analog Discovery for the offset to stabilize, before the first reading after device open or offset/range change
time.sleep(2)

print("Starting repeated acquisitions")
dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

for iTrigger in range(N_run):
    # new acquisition is started automatically after done state 

    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if sts.value == DwfStateDone.value :
            break
        time.sleep(0.001)
    
    dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples1, Num_Samples) # get channel 1 data
    dwf.FDwfAnalogInStatusData(hdwf, 1, rgdSamples2, Num_Samples) # get channel 2 data
    
    dc = sum(rgdSamples1)/len(rgdSamples1)
    print("Acquisition #"+str(iTrigger)+" average: "+str(dc)+"V")
    plt.plot(rgdSamples2)
    Total = Total + rgdSamples2
    
    sec = c_uint()
    tick = c_uint()
    ticksec = c_uint()
    # acquisition software time for Analog Discovery and T0 with 8-10ns precision for ADP3X50
    dwf.FDwfAnalogInStatusTime(hdwf, byref(sec), byref(tick), byref(ticksec))
    s = time.localtime(sec.value)
    ns = 1e9/ticksec.value*tick.value
    ms = math.floor(ns/1e6)
    ns -= ms*1e6
    us = math.floor(ns/1e3)
    ns -= us*1e3
    ns = math.floor(ns)
    print(time.strftime("%Y-%m-%d %H:%M:%S", s)+"."+str(ms).zfill(3)+"."+str(us).zfill(3)+"."+str(ns).zfill(3))
    
dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(0))
dwf.FDwfDeviceCloseAll()

#plt.plot(rgdSamples1)

plt.show()
plt.plot(rgdSamples2)
plt.plot(Total/N_run)
plt.show()
# plt.plot(numpy.fromiter(rgdSamples, dtype = numpy.float))
# plt.show()

