import time
import tidevice

t = tidevice.Device("00008030-0015293E0EE0802E")
perf = tidevice.Performance(t, perfs=list(tidevice.DataType))


def callback(_type: tidevice.DataType, value: dict):
    writefile = open(
        # logpath + 'iOS' + str(case_name) + '@' + str(version) + '@' + str(devices) + '@' + str(now) + '@' + str(
        #     os .getpid()) + '.log', 'a+' )
    if _type.value =='cpu':
        writefile.write('cpu,%s,%sln' % (value['timestamp '], numpy . round (value[ 'value'], 2)))
    elif _type.value == 'memory' :
         writefile .write( ' memory,%s ,%sln' % (value[ ' timestamp' ], numpy. round(value[ 'value'], 2)))
    elif _type.value == 'fps' :
         writefile.write('fps,%s,%sln' % (value['timestamp' ], numpy . round(value[ 'value'], 2)))
    elif _type.value ==' network ' :
         writefile .write(' network,%s,%s,%sln'% (
             value[ 'timestamp' ], numpy . round(value['downFlow'], 2), numpy . round(value[ 'upFlow'], 2)))
         print( 'done' )
    writefile.close()


perf.start("com.dev8.mojomaker", callback=callback)
time.sleep(30)
perf.stop()