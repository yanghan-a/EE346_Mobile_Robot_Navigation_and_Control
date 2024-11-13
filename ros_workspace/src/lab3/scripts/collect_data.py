#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

# 初始化数据列表
data = []

# 回调函数
def callback(scan):
    global data
    # 提取 ranges 列表中的第一个元素
    if scan.ranges:
        first_range = scan.ranges[0]
        
        # 只收集非零值
        if first_range != 0:
            data.append(first_range)
            print(len(data))

            # 检查数据是否已达到 100 组
            if len(data) >= 200:
                write_to_file(data)
                rospy.signal_shutdown("Collected 200 valid data points.")

def write_to_file(data):
    # 将数据写入 txt 文件
    with open('110.txt', 'w') as file:
        for value in data:
            file.write(f"{value}\n")
    rospy.loginfo("Data written to scan_data.txt")

def listener():
    # 初始化 ROS 节点
    rospy.init_node('laser_scan_listener', anonymous=True)
    
    # 订阅 /scan 话题
    rospy.Subscriber('/scan', LaserScan, callback)
    
    # 循环等待消息
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
