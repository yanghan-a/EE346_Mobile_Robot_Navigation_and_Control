import rospy
import actionlib
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion
import numpy as np
import time
import itertools
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped

# 定义状态
NAVIGATION = 0
DETECT =1
STOP = 2
STOP_2S = 3

# 初始化状态
current_state = NAVIGATION

# 目标位置
# target_poses = [(2.51,4.0),(0.14, 3.55), (-0.62, -0.05), (2.4, 0.56)]  
target_poses = [(2.51,4.0), (1.52,3.74),(0.14, 3.55),(0.96,1.64),(-0.62, -0.05), (2.4, 0.56)]  
detect_or_not = [False,     False,      True,         False,      True,          True]
# 起点坐标(2.51,4.0),2-3之间补充点(0.96,1.64),1-2之间补充点(1.52,3.74)
current_target_index = 1

current_position_x = 0
current_position_y = 0

current_pose_x = 0
current_pose_y = 0
current_pose_z = 0
current_pose_w = 0
# 初始化发布者
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
pub_pose = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
navigate = True

delay_counter = 0

navigate_delay = 0
def navigate_to_target():
    global current_target_index
    global navigate,navigate_delay
    target_pose = target_poses[current_target_index]  # 获取当前目标位置

    if navigate:
        
        # # 初始化 move_base 客户端
        # client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

        # rospy.loginfo(f"Navigating to target: {target_pose}")

        # # 等待 action server 启动
        # client.wait_for_server()

        # # 创建 MoveBaseGoal
        # goal = MoveBaseGoal()
        
        # # 设置目标位置（假设目标位置是一个 2D 坐标 (x, y)）
        # goal.target_pose.header.frame_id = "map"  # 使用地图坐标系
        # goal.target_pose.header.stamp = rospy.Time.now()

        # # 设置目标位置的坐标和朝向
        # goal.target_pose.pose.position = Point(target_pose[0], target_pose[1], 0.0)  # 目标位置
        # goal.target_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 1.0)  # 朝向（这里假设没有旋转）

        # # 发送目标到 move_base 并等待执行结果
        # client.send_goal(goal)

        # 等待目标完成
        # client.wait_for_result()

        


        # 构造 PoseStamped 消息
        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"  # 目标位置的参考坐标系
        goal_msg.header.stamp = rospy.Time.now()  # 当前时间戳

        # 设置目标位置 (x, y, z)
        goal_msg.pose.position.x = target_pose[0]
        goal_msg.pose.position.y = target_pose[1]
        goal_msg.pose.position.z = 0.0

        # 设置目标朝向 (使用四元数表示)
        goal_msg.pose.orientation.x = current_pose_x
        goal_msg.pose.orientation.y = current_pose_y
        goal_msg.pose.orientation.z = current_pose_z
        goal_msg.pose.orientation.w = current_pose_w
        pub_pose.publish(goal_msg)

        # navigate = False
    #     return False
    # else:
        rospy.loginfo("正在执行导航到点任务！")
        # 检查导航是否成功
        if abs(current_position_x-target_pose[0])<0.5 and abs(current_position_y-target_pose[1])<0.5:
            rospy.loginfo("Successfully reached the target!")
            navigate_delay = navigate_delay+1
            if navigate_delay>5:
            # navigate = False
                navigate_delay = 0
                return True
            else:
                return False
        else:
            return False


def detect_and_stop(scan_data):
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
    list = process_ranges(ranges)

    return publish_vel(list,ranges)


def state_machine(scan_data):
    global navigate
    global current_state
    global current_target_index
    global delay_counter
    if current_state == NAVIGATION:
        if navigate_to_target():
            if detect_or_not[current_target_index]:
                current_state = DETECT
            else:
                current_state = NAVIGATION
                current_target_index = (current_target_index + 1) % len(target_poses)
    if current_state ==DETECT:
        if detect_and_stop(scan_data):  
            current_state = STOP  # 切换到检测停止状态

    elif current_state == STOP:
        if delay_counter<12:
            rospy.loginfo("正在执行延时等待")
            delay_counter = delay_counter+1
            twist = Twist()
            pub.publish(twist)
        else:
            current_state = STOP_2S  # 切换到停止 2 秒状态
            delay_counter=0
            navigate = True

    elif current_state == STOP_2S:
        # 结束当前目标，开始下一个目标
        current_target_index = (current_target_index + 1) % len(target_poses)
        current_state = NAVIGATION  # 切换回导航状态


def find_small_key_diff_combinations(largest_diff_dict, ranges,threshold=25):
    # 获取字典中的所有键
    keys = list(largest_diff_dict.keys())

    # 存储差值小于 threshold 的键组合
    valid_combinations = []

    # 生成所有键的两两组合
    for (key1, key2) in itertools.combinations(keys, 2):
        # 计算键的差值
        diff = abs(key1 - key2)
        average_key_o = 0
        if diff>180:
            average_key = round((key1+key2-360)/2)
            if average_key<0:
                average_key = average_key +360
                
        else:
            average_key = round((key1+key1)/2)
        average_key_o = average_key
        if average_key>180:
            average_key = average_key-360
        # 如果差值小于给定的阈值，添加到 valid_combinations 中
        # if diff < threshold:
        valid_combinations.append((average_key, diff,average_key_o))
    distance = 100
    index_modi = 0
    diff = 0
    index = 0
    for i in valid_combinations:
        a,b ,c= i
        if ranges[c]<distance:
            distance = ranges[c]
            index_modi = a
            diff = b
            index = c

    goal = [index_modi,diff, index]
    return goal

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

    # # 获取最大的两个差分值及其索引
    # threshold = 0.5  # 要找的最大数个数    
    # # 只返回包含最大差分值的字典
    # filtered_diff_dict = {k: v for k, v in sorted_diff_dict.items() if v > threshold}

    # 获取最大的前5个差分值及其索引
    top_n = 8  # 选择前5个最大的差分值

    filtered_diff_dict = {k: sorted_diff_dict[k] for k in list(sorted_diff_dict.keys())[:top_n]}


    largest_indices_sorted = list(filtered_diff_dict.keys())

    print(f"最大差分值的索引: {largest_indices_sorted}")
    print(f"最大差分值: {list(filtered_diff_dict.values())}")
    list1 = []
    list1 = find_small_key_diff_combinations(filtered_diff_dict,ranges,15)
    print("最终的目标，调整索引、夹角、原始索引",list1)
    return list1

def publish_vel(list1,ranges):
    global pub
    # total_diff_sum = sum(diff_dict.values())
    # average_value = total_diff_sum/len(diff_dict)
    # 对字典的键求和
    # 获取排序后的键列表
    # sorted_keys = list(diff_dict.keys())
    
    # 取出索引1和2的键值对
    
    distance = ranges[list1[2]]

    print("目标距离",distance)
    kw = 0.05
    kl = 0.8
    twist = Twist()

    print("夹角",list1[1])
    # if list1[1] < 25:
    if distance  > 0.2:

        twist.linear.x =  kl*distance # X 轴的线速度
        twist.angular.z = kw*list1[0]  # 绕 Z 轴的角速度
        pub.publish(twist)
        return False
    else:
        twist.linear.x =  0# X 轴的线速度
        twist.angular.z = 0  # 绕 Z 轴的角速度
        pub.publish(twist)
    
        return True

def scan_callback(scan_data):
    # 执行状态机
    state_machine(scan_data)

def amcl_pose_callback(msg):
    global current_position_x, current_position_y
    global current_pose_x, current_pose_y,current_pose_z,current_pose_w
    # 提取x和y坐标
    current_position_x = msg.pose.pose.position.x
    current_position_y = msg.pose.pose.position.y

    current_pose_x = msg.pose.pose.orientation.x
    current_pose_y = msg.pose.pose.orientation.y
    current_pose_z = msg.pose.pose.orientation.z
    current_pose_w = msg.pose.pose.orientation.w
    rospy.loginfo(f"AMCL Pose: x={current_position_x}, y={current_position_y}")


def listener():
    rospy.init_node('robot_control', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, scan_callback)
    rospy.Subscriber("/amcl_pose",PoseWithCovarianceStamped,amcl_pose_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
