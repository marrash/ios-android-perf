#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import time
import tidevice


t = tidevice.Device('00008030-0015293E0EE0802E')
perf = tidevice.Performance(t,perfs=list(tidevice.DataType))


def callback(_type: tidevice.DataType, value: dict):
    print("R:", _type.value, value)


perf.start("com.dev8.mojomaker", callback=callback)
time.sleep(30)
perf.stop()