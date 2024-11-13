#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

# 初始化最大值和最小值
max_range = float('-inf')
min_range = float('inf')

# 回调函数
def callback(scan):
    global max_range, min_range
    # 提取 ranges 列表中的第一个元素
    if scan.ranges:
        first_range = scan.ranges[0]
        
        # 更新最大值和最小值
        if first_range > max_range:
            max_range = first_range
        
        if first_range < min_range and first_range > 0:  # 避免考虑零值
            min_range = first_range
        
        rospy.loginfo(f'First range: {first_range}, Max: {max_range}, Min: {min_range}')

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
