#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix

def callback(data):
    rospy.loginfo(data)
    
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("map", NavSatFix, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

