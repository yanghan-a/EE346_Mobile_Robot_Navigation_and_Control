import rospy
from sensor_msgs.msg import LaserScan
import numpy as np
from geometry_msgs.msg import Twist
import itertools
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


def find_small_key_diff_combinations(largest_diff_dict, threshold=25,ranges):
    # 获取字典中的所有键
    keys = list(largest_diff_dict.keys())

    # 存储差值小于 threshold 的键组合
    valid_combinations = []

    # 生成所有键的两两组合
    for (key1, key2) in itertools.combinations(keys, 2):
        # 计算键的差值
        diff = abs(key1 - key2)
        
        # 如果差值小于给定的阈值，添加到 valid_combinations 中
        if diff < threshold:
            valid_combinations.append((key1, key2, diff))

    return valid_combinations

def process_ranges(ranges):
    # 标记异常值：将 ranges 中为 0 的值标记为异常
    # abnormal_indices = np.where(ranges == 0)[0]
    # print(f"异常值的索引: {abnormal_indices}")

    # 对 ranges 做差分并取绝对值
    diff_abs = np.abs(np.diff(ranges))

    # 创建一个字典来存储差分值和对应的索引
    diff_dict = {i: diff_abs[i] for i in range(len(diff_abs))}
    
    # 按照差分值排序字典（从大到小）
    sorted_diff_dict = {k: v for k, v in sorted(diff_dict.items(), key=lambda item: item[1], reverse=True)}

    # 获取最大的两个差分值及其索引
    threshold = 1  # 要找的最大数个数    
    # 只返回包含最大差分值的字典
    filtered_diff_dict = {k: v for k, v in sorted_diff_dict.items() if v > threshold}

    largest_indices_sorted = list(filtered_diff_dict.keys())

    print(f"最大差分值的索引: {largest_indices_sorted}")
    print(f"最大差分值: {list(filtered_diff_dict.values())}")
    list1 = []
    list1 = find_small_key_diff_combinations(filtered_diff_dict,25,ranges)
    print(list1)
    return list1

def publish_vel(list,ranges):
    global pub
    a,b,c = list[0]
    # total_diff_sum = sum(diff_dict.values())
    # average_value = total_diff_sum/len(diff_dict)
    # 对字典的键求和
    # 获取排序后的键列表
    # sorted_keys = list(diff_dict.keys())
    
    # 取出索引1和2的键值对
    key1 = a
    key2 = b
    
    # 计算它们的差值
    value_diff = abs(key1 - key2)
    if value_diff>180:
        average_key = round((key1+key2-360)/2)
        if average_key<0:
            average_key = average_key +360
    else:
        average_key = round((key1+key1)/2)

    if average_key>180:
        average_key = average_key-360


    print("average_key",average_key)
    distance = ranges[average_key]

    print("distance",distance)
    kw = 0.2
    kl = 0.5
    twist = Twist()

    if c < 25:
        twist.linear.x =  kl*distance # X 轴的线速度
        twist.angular.z = kw*average_key  # 绕 Z 轴的角速度
        # pub.publish(twist)
    else:
        twist.linear.x =  0# X 轴的线速度
        twist.angular.z = 0  # 绕 Z 轴的角速度
        # pub.publish(twist)
    


def scan_callback(scan_data):
    ranges = np.array(scan_data.ranges)
    # 特殊情况：处理前几个值为0的情况
    for i in range(len(ranges)):
        if ranges[i] == 0:  # 遇到0值
            if i == 0:  # 第一个值是0
                # 用后一个有效值填充
                for j in range(i + 1, len(ranges)):
                    if ranges[j] != 0:
                        ranges[i] = ranges[j]
                        break
            else:
                # 用前一个有效值填充
                ranges[i] = ranges[i - 1]

    # 打开文件并将数据追加写入
    # with open("laser_ranges1.txt", "a") as file:  # 使用 'a' 模式来追加
    #     # 写入 ranges 数据
    #     for value in ranges:
    #         file.write(f"{value}\n")
        
    #     # 写入分隔符
    #     file.write("----------\n")
    
    # rospy.loginfo("Ranges data has been written to laser_ranges1.txt")

    list = process_ranges(ranges)
    publish_vel(list,ranges)


def listener():
    rospy.init_node('scan_listener', anonymous=True)
    
    rospy.Subscriber("/scan", LaserScan, scan_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
