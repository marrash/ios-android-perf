#!/usr/bin/env python
# coding:utf-8
"""
Name : FpsInfo.py
Author  :
Contect : 
Time    : 2020/7/21 14:26
Desc:
"""


class FpsInfo(object):
    def __init__(self, time, total_frames, fps, pkg_name, window_name, jankys_ary, jankys_more_than_16,
                 jankys_more_than_166,cpukel,memory,cpu_usage,sys_cpu,_flow_d,_flow_u,temperature,battery):
        # 采样数据时的时间戳
        self.time = time
        # 2s内取到总帧数
        self.total_frames = total_frames
        # fps
        self.fps = fps
        # 测试应用包名
        self.pkg_name = pkg_name
        # 窗口名
        self.window_name = window_name
        # 掉帧具体时间集合
        self.jankys_ary = jankys_ary
        # 掉帧数目,大于16.67ms
        self.jankys_more_than_16 = jankys_more_than_16
        # 卡顿数目,大于166.7ms
        self.jankys_more_than_166 = jankys_more_than_166
        # cpu核心
        self.cpukel = cpukel
        # memory
        self.memory = memory
        # cpu
        self.cpu_usage = cpu_usage
        # sys_cpu
        self.sys_cpu = sys_cpu
        # wifi 下載流量
        self._flow_d = _flow_d
        # wifi 上傳流量
        self._flow_u = _flow_u
        # 溫度
        self.temperature = temperature
        # 剩餘電量
        self.battery = battery
   