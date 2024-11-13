#!/usr/bin/env python

from cmath import atan
import math
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class vel_manipulator():
    
    def __init__(self):

        pub_topic_name = "/turtle1/cmd_vel"
        sub_topic_name = "/turtle1/pose"

        self.pub = rospy.Publisher(pub_topic_name,Twist,queue_size = 10)
        self.number_subscriber = rospy.Subscriber(sub_topic_name,Pose,self.pose_callback)
        self.velocity_msg = Twist()
        self.theta = 0
        self.wall = 0
        self.judge = True

        self.reverse_angle = 3.14
        self.reverse_velocity = 0

        self.acc_angle = 0
        self.last_angle = 0
        self.pi = 3.1415926
    def pose_callback(self,msg):
        if(msg.theta-self.last_angle>self.pi):
            delta_angle = msg.theta-self.last_angle-self.pi*2
        elif(msg.theta-self.last_angle<-self.pi):
            delta_angle = 2*self.pi+(msg.theta-self.last_angle)
        else:
            delta_angle = msg.theta-self.last_angle
        self.acc_angle = self.acc_angle+delta_angle
        self.last_angle = msg.theta

        if((msg.x <=2  or msg.x >= 8 or msg.y <= 2 or msg.y >= 8)and self.wall==0):
            self.wall = 1
            if(msg.x<=2):
                self.reverse_velocity = 6.28 if(msg.y>=5) else -6.28
            elif(msg.x>=8):
                self.reverse_velocity = -6.28 if(msg.y>=5) else 6.28
            elif(msg.y<=2):
                self.reverse_velocity = -6.28 if(msg.x>=5) else 6.28
            elif(msg.y>=8):
                self.reverse_velocity = 6.28 if(msg.x>=5) else -6.28
        if(msg.x <8  and msg.x > 2 and msg.y < 8 and msg.y > 2 and self.wall==2):
            self.wall = 0
            self.velocity_msg.linear.x = 0
            self.pub.publish(self.velocity_msg)
        if(msg.x >=8  or msg.x <= 2 or msg.y >= 8 or msg.y <= 2 or self.wall==2):
            theta = math.atan2(5-msg.y,5-msg.x)
            if(msg.theta>theta-0.2 and msg.theta<theta+0.2 ):
                self.velocity_msg.angular.z = 0
                self.velocity_msg.linear.x = 1.5
            else:
                self.velocity_msg.angular.z = 1.5
                
            self.pub.publish(self.velocity_msg)
        if(self.wall==1):
            if(self.judge):
                self.theta = self.acc_angle
                self.judge = False

        if(not self.judge):
            if(self.reverse_velocity>0):
                d_theta = self.acc_angle-self.theta
                if(d_theta >= self.reverse_angle):
                    self.velocity_msg.angular.z = 0
                    self.velocity_msg.linear.x = 1.5
                    self.judge = True
                    self.wall=2
                else:
                    self.velocity_msg.angular.z = self.reverse_velocity
            else:
                d_theta = self.acc_angle-self.theta
                if(d_theta <= -self.reverse_angle):
                    self.velocity_msg.angular.z = 0
                    self.velocity_msg.linear.x = 0
                    self.judge = True
                    self.wall=2
                else:
                    self.velocity_msg.angular.z = self.reverse_velocity
            self.pub.publish(self.velocity_msg)
        

if __name__ == '__main__':
    node_name = "turtlebot_saver"
    rospy.init_node(node_name, anonymous=True)
    vel_manipulator()
    rospy.spin()

