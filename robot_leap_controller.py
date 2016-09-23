#!/usr/bin/env python
#author:rohan
#ROS node to control the robot by using linear and angular velocities from the leap motion sensor
#importing library    
from beginner_tutorials.srv import *
import rospy
import rospy
from geometry_msgs.msg import Vector3, Twist   
#callback method for the subscriber
def callback(data):
    #scaling down the linear and angular velocities
    v=data.x/50
    w=data.y/50
    #Calling publisher function to send the data received to the robot
    publisher(v,w);
    return 0
#publishing the linear and angular velocities to the robot
def publisher (v,w): 
    pub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(0.01)
    try : 
	tw = Twist(Vector3(v,0,0), Vector3(0,0,w))
	pub.publish(tw)
	print "Data sent to robot"
	#rate.sleep()
    except  rospy.ROSInterruptException:
	pass
    return 0
#subscribing to the topic leap_chatter which contains the control inputs
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('leap_chatter', Vector3, callback)
    rospy.spin()  
#main function 
if __name__ == "__main__":
       listener()
