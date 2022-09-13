import time
import tidevice

t = tidevice.Device("00008030-0015293E0EE0802E")
perf = tidevice.Performance(t, perfs=list(tidevice.DataType))


def callback(_type: tidevice.DataType, value: dict):
    # print("R:", _type.value, value)
    # if _type.value == "fps":
    #     print(value)
        # with open("fpslog.txt", "a+") as fpslog:
        #     fpslog.write(str(value) + "\n")
    if _type.value == "cpu":
        print(value)
        # with open("cpulog.txt", "a+") as cpulog:
        #     cpulog.write(str(value) + "\n")
    if _type.value == "memory":
        print(value)
        # with open("memorylog.txt", "a+") as memorylog:
        #     memorylog.write(str(value) + "\n")


perf.start("com.dev8.mojomaker", callback=callback)
time.sleep(10)
perf.stop()