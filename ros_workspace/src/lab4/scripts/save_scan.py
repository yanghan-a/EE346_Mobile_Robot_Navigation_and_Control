#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

# 定义回调函数，用于处理接收到的激光扫描数据
def scan_callback(msg):
    # 获取 ranges 数组数据
    ranges = msg.ranges
    
    # 打开文件并将数据追加写入
    with open("laser_ranges1.txt", "a") as file:  # 使用 'a' 模式来追加
        # 写入 ranges 数据
        for value in ranges:
            file.write(f"{value}\n")
        
        # 写入分隔符
        file.write("----------\n")
    
    rospy.loginfo("Ranges data has been written to laser_ranges1.txt")

def listener():
    # 初始化 ROS 节点
    rospy.init_node('laser_scan_listener', anonymous=True)

    # 订阅 /scan 话题
    rospy.Subscriber('/scan', LaserScan, scan_callback)

    # 保持节点运行，直到节点被关闭
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
