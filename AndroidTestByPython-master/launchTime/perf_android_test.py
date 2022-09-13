'''
@author fenfenzhong
'''
# encoding:utf-8
from cgi import print_directory
import csv
import imp
from tkinter.tix import Form
from click import File
from cv2 import line
from numpy import power
from pydantic import validator
import pymysql.cursors
from asyncore import loop
import os
import re
import subprocess
import time
from pydantic import validator

from FpsListenserImpl import FpsListenserImpl 


# 變數
pkg_name = "com.heytap.browser"#测试应用包名称  Chrome: com.android.chrome  UC瀏覽器: com.UCMobile
devices = "YLE64LRS49ZLWCKN"#裝置ID cmd :adb device  #oppo: YLE64LRS49ZLWCKN  華為: 5VSNW19517003630
app_bundle_id = "com.heytap.browser/com.android.browser.BrowserActivity" #测试应用Activity名称 com.android.chrome/com.google.android.apps.chrome.Main   com.UCMobile/com.uc.browser.InnerUCMobile
adb="C:\platform-tools\adb.exe" #本地adb路径
num = 1 #資料執行次數


# 啟動APP
def launch_app():
    cmd = "adb shell am start -n " + app_bundle_id  # type: str
    os.popen(cmd)
# 停止app
def stop_app():
    cmd = 'adb shell input keyevent 3'
    os.popen(cmd)

# 獲得當前時間
def get_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("time :",current_time)
    return current_time
# 獲取memory
def get_mem(pkg_name,devices):
    cmd = "adb -s " +  devices +" shell  dumpsys  meminfo %s" % (pkg_name)
    #print(cmd)
    output = subprocess.check_output(cmd).split()
    s_men = ".".join([x.decode() for x in output]) # 转换为string
    #print(s_men)
    #擷取TOTAL.後的字串
    men2 = int(re.findall("TOTAL.(\d+)*", s_men, re.S)[0])
    print("mem :",round(men2,2),"K,",round(men2/1024,2),"M")

# 獲得電池溫度
def get_temp():
    cmd = "adb shell dumpsys battery"
    output = subprocess.check_output(cmd).split()
    ss =str(output)
    appptemp=ss.split("temperature:', b'")[1].split("',")[0]
    temp = int(appptemp)
    print("temp :",temp/10,"℃")

# 獲取fps
'''
def get_fps():
    each_frame_timestamps = []
    timestamps = []
    cmd_clear = "adb shell dumpsys gfxinfo " + pkg_name + " reset"
    os.popen(cmd_clear)
    #print(cmd_clear)
    #cmd = "adb shell dumpsys SurfaceFlinger --latency " + app_bundle_id + "#0"
    cmd = "adb shell dumpsys gfxinfo " + pkg_name + " framestats"
    output = subprocess.check_output(cmd).split()
    #print(cmd)

    results = os.popen(cmd).read().strip()
    #print("results :",results)

    frames = [x for x in results.split('\n') if validator(x)]
    frame_count = len(frames)
    jank_count = 0
    caton = 0
    vsync_overtime = 0
    render_time = 0
    for frame in frames:
        time_block = re.split(r'\s+', frame.strip())
        if len(time_block) == 3:
            try:
                render_time = float(time_block[0]) + float(time_block[1]) + float(time_block[2])
            except Exception as e:
                render_time = 0    
        #print("render_time :",render_time)
        
        当渲染时间大于16.67，按照垂直同步机制，该帧就已经渲染超时
        那么，如果它正好是16.67的整数倍，比如66.68，则它花费了4个垂直同步脉冲，减去本身需要一个，则超时3个
        如果它不是16.67的整数倍，比如67，那么它花费的垂直同步脉冲应向上取整，即5个，减去本身需要一个，即超时4个，可直接算向下取整

        最后的计算方法思路：
        执行一次命令，总共收集到了m帧（理想情况下m=128），但是这m帧里面有些帧渲染超过了16.67毫秒，算一次jank，一旦jank，
        需要用掉额外的垂直同步脉冲。其他的就算没有超过16.67，也按一个脉冲时间来算（理想情况下，一个脉冲就可以渲染完一帧）

        所以FPS的算法可以变为：
        m / （m + 额外的垂直同步脉冲） * 60
        
        if render_time > 16.67:
            jank_count += 1
            if render_time % 16.67 == 0:
                vsync_overtime += int(render_time / 16.67) - 1
            else:
                vsync_overtime += int(render_time / 16.67)
        if render_time >166.7:
            caton += 1

    _fps = int(frame_count*60 / (frame_count + vsync_overtime))
    print("jank_count :",jank_count,"\ncaton :",caton,"\nframe_count :",frame_count,"\nfps :",_fps)
    jank = str(jank_count)
    frame = str(frame_count)
    fps = str(_fps)
    # return (frame_count, jank_count, fps)
    
    # 連接資料庫
    connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='Super81444166',
    db='android_test',
    charset='utf8'
    )
    # 寫入資料
    cursor = connect.cursor()
    sql = "INSERT INTO and_fps (jank_count,frame_count,_fps) VALUES('"+jank+"','"+frame+"','"+fps+"')"
    cursor.execute(sql)
    connect.commit()
    # 关闭连接
    cursor.close()
    connect.close()
    '''


# 獲取cpu核心數量
def get_cpu_kel(devices):
    adb = "adb -s " + devices + " shell cat /proc/cpuinfo"
    #print(adb)
    output = subprocess.check_output(adb).split()
    sitem = ".".join([x.decode() for x in output])  # 转换为string
    print("CPU核心 :",len(re.findall("processor", sitem)))
    cpukel = len(re.findall("processor", sitem))
    return cpukel

# 取得APP的pid
def get_pid(devices,pkg_name):
    adb = "adb -s " + devices + " shell dumpsys meminfo " + pkg_name
    #print(adb)
    output = subprocess.check_output(adb).split()
    ss =str(output)
    apppid=ss.split("'pid', b'")[1].split("',")[0]
    #print("app pid :",apppid)
    return apppid

# 取得APP的cpu 使用率
'''
 每一个cpu快照均
'''
def totalCpuTime(devices):
    user=nice=system=idle=iowait=irq=softirq= 0
    '''
    user:从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
    nice:从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
    system 从系统启动开始累计到当前时刻，处于核心态的运行时间
    idle 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
    iowait 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
    irq 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
    softirq 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
    stealstolen  这是时间花在其他的操作系统在虚拟环境中运行时（since 2.6.11）
    guest 这是运行时间guest 用户Linux内核的操作系统的控制下的一个虚拟CPU（since 2.6.24）
    '''
    cmd = "adb -s " + devices +" shell cat /proc/stat"
    #print("cmd :",cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res = output.split()
    for info in res:
        if info.decode() == "cpu":
            user = res[1].decode()
            nice = res[2].decode()
            system = res[3].decode()
            idle = res[4].decode()
            iowait = res[5].decode()
            irq = res[6].decode()
            softirq = res[7].decode()
            '''
            print("--------------------------------")
            print("user=" + user)
            print("nice=" + nice)
            print("system=" + system)
            print("idle=" + idle)
            print("iowait=" + iowait)
            print("irq=" + irq)
            print("softirq=" + softirq)
            '''
            
            result = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
            #print("totalCpuTime :"+str(result))
            return result

'''
每一个进程快照
'''
def processCpuTime(pid, devices):
    '''

    pid     进程号
    utime   该任务在用户态运行的时间，单位为jiffies
    stime   该任务在核心态运行的时间，单位为jiffies
    cutime  所有已死线程在用户态运行的时间，单位为jiffies
    cstime  所有已死在核心态运行的时间，单位为jiffies
    '''
    cmd = "adb -s " + devices +" shell cat /proc/stat"
    #print(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res = output.split()
    #print("res :",res)
    utime = res[13].decode()
    stime = res[14].decode()
    cutime = res[15].decode()
    cstime = res[16].decode()
    
    '''
    print("utime="+utime)
    print("stime="+stime)
    print("cutime="+cutime)
    print("cstime="+cstime)
    '''
    result = int(utime) + int(stime) + int(cutime) + int(cstime)
    return result

'''
计算某进程的cpu使用率
100*( processCpuTime2 – processCpuTime1) / (totalCpuTime2 – totalCpuTime1) (按100%计算，如果是多核情况下还需乘以cpu的个数);
cpukel cpu几核
pid 进程id
'''
def cpu_rate(devices):
    # pid = get_pid(pkg_name)
    #print("processCpuTime :",processCpuTime(pid, devices))
    processCpuTime1 = processCpuTime(get_pid(devices,pkg_name), devices)
    time.sleep(1)
    processCpuTime2 = processCpuTime(get_pid(devices,pkg_name), devices)
    processCpuTime3 = processCpuTime2 - processCpuTime1

    totalCpuTime1 = totalCpuTime(devices)
    time.sleep(1)
    totalCpuTime2 = totalCpuTime(devices)
    totalCpuTime3 = (totalCpuTime2 - totalCpuTime1)*get_cpu_kel(devices)

    cpu = 100 * (processCpuTime3) / (totalCpuTime3)*get_cpu_kel(devices)
    #print("processCpuTime :",processCpuTime(pid, devices))
    print("USE_CPU :",round(cpu,2),"%")


'''
# 获取热启动时间
def get_launched_time():
    for line in content.open.read:
        line = line.strip()
        if "ThisTime" in line:
            startTime = line.split(":")[1]
            #print (self.startTime)
        if "TotalTime" in line:
            startTime2 = line.split(":")[1]
            #print (self.startTime2)
        if "WaitTime" in line:
            startTime3 = line.split(":")[1] 
            #print (self.startTime3) 
                        
        print (startTime,startTime2,startTime3)
'''

#啟動APP
launch_app()

#取得APP數值
for _ in range(num):
    get_mem(pkg_name,devices)
    get_temp()
    #get_fps()
    get_pid(devices,pkg_name)
    cpu_rate(devices)
    get_time()
    #get_launched_time()
    #time.sleep(1)
    print("------------------------------------")

#停止APP
#stop_app()