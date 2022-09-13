import re
import subprocess
import time
import pymysql
from FpsListener import IFpsListener


class FpsListenserImpl(IFpsListener):
    def __init__(self):
        pass

    def report_fps_info(self, fps_info):
        print('\n')
        #print("当前设备是：" + fps_info.)
        print("當前進程：" + str(fps_info.pkg_name))
        print("當前窗口是：" + str(fps_info.window_name))
        print("當前手機窗口刷新時間：" + str(fps_info.time))
        print("當前窗口fps：" + str(fps_info.fps))
        print("當前2s獲取總幀數：" + str(fps_info.total_frames))
        print("當前窗口丢幀數(>16.67ms）：" + str(fps_info.jankys_more_than_16))
        #print(fps_info.jankys_ary)
        print("當前窗口卡顿數(>166.7ms)：" + str(fps_info.jankys_more_than_166))
        #print("卡頓次數 :", str(fps_info.caton_count))
        print("CPU核心 :",str(fps_info.cpukel))
        print("應用的CPU使用率 :",str(fps_info.cpu_usage),"%")
        print("系統CPU使用率 :",str(fps_info.sys_cpu),"%")
        print("記憶體 :",str(fps_info.memory),"M")
        print("wifi下載流量 :",str(fps_info._flow_d))
        print("wifi上傳流量 :",str(fps_info._flow_u))
        print("溫度 :",str(fps_info.temperature),"°C")
        print("當前電量 :",str(fps_info.battery),"%")
        print('\n')

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
        sql = "INSERT INTO and_fps (jank,big_jank,frame_count,_fps,time_fps) VALUES('"+str(fps_info.jankys_more_than_16)+"','"+str(fps_info.jankys_more_than_166)+"','"+str(fps_info.total_frames)+"','"+str(fps_info.fps)+"','"+str(fps_info.time)+"')"
        sql_cpu = "INSERT INTO and_cpu (cpukel,use_cpu,sys_cpu,temperature,time_cpu) VALUES('"+str(fps_info.cpukel)+"','"+str(fps_info.cpu_usage)+"','"+str(fps_info.sys_cpu)+"','"+str(fps_info.temperature)+"','"+str(fps_info.time)+"')"
        sql_mem = "INSERT INTO and_memory (memory,time_memory) VALUES('"+str(fps_info.memory)+"','"+str(fps_info.time)+"')"
        sql_net = "INSERT INTO and_network (netflow_download,netflow_upload,time_net) VALUES('"+str(fps_info._flow_d)+"','"+str(fps_info._flow_u)+"','"+str(fps_info.time)+"')"
        cursor.execute(sql)
        cursor.execute(sql_cpu)
        cursor.execute(sql_mem)
        cursor.execute(sql_net)
        connect.commit()
        # 关闭连接
        cursor.close()
        connect.close()
