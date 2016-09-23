#!/usr/bin/env python
__author__ = 'rohan'
#ROS Node to identify gestures,count fingers and measure hand palm position and orientation
#importing libraries
import sys
import rospy
from client_server.srv import *
import math
import rospy
from leap_motion.msg import leap
from leap_motion.msg import leapros
from geometry_msgs.msg import Point
import rospy 
from geometry_msgs.msg import Vector3, Twist
gesture_recog = 1;
#callback function for subscriber topic leapmotion/data
def callback(data):
    # retreiving all finger joint locations/palm position and direction in real-time
    global gesture_recog
    direction_indicator = data.direction.x
    hand_direction_x = data.direction.x
    hand_direction_y = data.direction.y
    finger5_metacarpal_y = data.pinky_metacarpal.y;
    finger5_proximal_y = data.pinky_proximal.y;
    finger5_intermediate_y = data.pinky_intermediate.y;
    finger5_distal_y = data.pinky_distal.y;
    finger5_tip_y = data.pinky_tip.y;
    finger4_metacarpal_y = data.ring_metacarpal.y;
    finger4_proximal_y = data.ring_proximal.y;
    finger4_intermediate_y = data.ring_intermediate.y;
    finger4_distal_y = data.ring_distal.y;
    finger4_tip_y = data.ring_tip.y;
    finger3_metacarpal_y = data.middle_metacarpal.y;
    finger3_proximal_y = data.middle_proximal.y;
    finger3_intermediate_y = data.middle_intermediate.y;
    finger3_distal_y = data.middle_distal.y;
    finger3_tip_y = data.middle_tip.y;
    finger2_metacarpal_y = data.index_metacarpal.y;
    finger2_metacarpal_x = data.index_metacarpal.x;
    finger2_proximal_y = data.index_proximal.y;
    finger2_intermediate_y = data.index_intermediate.y;
    finger2_distal_y = data.index_distal.y;
    finger2_tip_y = data.index_tip.y;
    finger1_metacarpal_y = data.thumb_metacarpal.y;
    finger1_proximal_y = data.thumb_proximal.y;
    finger1_proximal_x = data.thumb_proximal.x;
    finger1_intermediate_y = data.thumb_intermediate.y;
    finger1_intermediate_x = data.thumb_intermediate.x;
    finger1_distal_y = data.thumb_distal.y;
    finger1_tip_y = data.thumb_tip.y;
    finger1_tip_x = data.thumb_tip.x;
    finger1_reference_x = 0.5*(data.thumb_intermediate.x+data.thumb_proximal.x);
    finger_count_copy = 0;
    hand_normal_y = data.normal.y;
    #controlling the translational speed of the robot for forward motion by discretizing linear velocity proportional to the finger count 
    if ((direction_indicator <0.5) and (direction_indicator > -0.5)):
        #detection of little finger
	if ((finger5_metacarpal_y < finger5_proximal_y) and (finger5_proximal_y < finger5_intermediate_y) and (finger5_intermediate_y < finger5_distal_y) and (finger5_distal_y < finger5_tip_y)):
        	flag_finger_5 = 1;
    	else:
		flag_finger_5 = 0;
        #detection of ring finger
    	if ((finger4_metacarpal_y < finger4_proximal_y) and (finger4_proximal_y < finger4_intermediate_y) and (finger4_intermediate_y < finger4_distal_y) and (finger4_distal_y < finger4_tip_y)):
        	flag_finger_4 = 1;
    	else:
		flag_finger_4 = 0;
        #detection of middle finger
    	if ((finger3_metacarpal_y < finger3_proximal_y) and (finger3_proximal_y < finger3_intermediate_y) and (finger3_intermediate_y < finger3_distal_y) and (finger3_distal_y < finger3_tip_y)):
        	flag_finger_3 = 1;
    	else:
		flag_finger_3 = 0;
        #detection of index finger
    	if ((finger2_metacarpal_y < finger2_proximal_y) and (finger2_proximal_y < finger2_intermediate_y) and (finger2_intermediate_y < finger2_distal_y) and (finger2_distal_y < finger2_tip_y)):
        	flag_finger_2 = 1;
    	else:
		flag_finger_2 = 0;
        #detection of thumb
    	if ((finger1_tip_x < finger1_reference_x)):
        	flag_finger_1 = 1;
    	else:
		flag_finger_1 = 0;
        #generating total finger count as a control input to determine translational speed
    	count_fingers = flag_finger_1+flag_finger_2+flag_finger_3+flag_finger_4+flag_finger_5;
    	print(flag_finger_1);
	print(flag_finger_2);
	print(flag_finger_3);
        print(flag_finger_4);
        print(flag_finger_5);
        print "******************";
	finger_count=flag_finger_1+flag_finger_2+flag_finger_3+flag_finger_4+flag_finger_5;
	print(finger_count);
	v=finger_count;
        gesture_recog = flag_finger_2+flag_finger_3+flag_finger_4+flag_finger_5;
	print "******************";
    #controlling the angular velocity of the robot proportional to the orientation of the hand about the z axis of leap motion
    #for controlling motion towards the left
    if (direction_indicator < 0):
        angle_rad = math.atan2(hand_direction_y, hand_direction_x);
	angle_deg = math.degrees(angle_rad);
        #angle varies from 0 to -90 degrees, maximum angle to the left is clamped at -90 (since cars will not turn more than 90 degrees) 
	if angle_deg > 0:
		angle_deg = 90-angle_deg
	else:
		angle_deg = -90;
	print(angle_deg);
        #the robot in this scenario can move with an linear velocity and a small angular velocity towards the left
	print "Speed and Direction Control Mode";
	print "Robot Moving Left";
	w = -angle_deg*0.1;
        #the robot in this scenario turns with an angular velocity towards the left
	if (direction_indicator < -0.5):
		print "Direction Control Mode";
		print "Robot Turning Left";
		print "Left";
                v=0;
    #for controlling motion towards the right
    elif (direction_indicator > 0):
	angle_rad = math.atan2(hand_direction_y, hand_direction_x);
	angle_deg = math.degrees(angle_rad);
        #angle varies from 0 to +90 degrees, maximum angle to the left is clamped at +90 (since cars will not turn more than 90 degrees) 
	if angle_deg > 0:
		angle_deg = 90-angle_deg
	else:
		angle_deg = 90;
	print(angle_deg);
        #the robot in this scenario can move with an linear velocity and a small angular velocity towards the right
	print "Speed and Direction Control Mode";
	print "Robot Moving Right";
 	w = -angle_deg*0.1;
        #the robot in this scenario turns with an angular velocity towards the right
	if (direction_indicator > 0.5):
		print "Direction Control Mode";
		print "Robot Turning Right";
		v=0;
    print "================================================"
    print(v);
    print(w);
    print "================================================"
    print "Transmit begins"
    #gesture recognition for car to stop
    if ((gesture_recog ==0) and (direction_indicator <0.5) and (direction_indicator > -0.5)):
	print "Stop";v=0;w=0;
    #gesture recognition for car to go in the backward/reverse direction by reversing the direction in which palm faces
    if (hand_normal_y > 0.2):
	print "Going Back";gesture_recog =1;v=-1;
    talker(v,w);
#listener module for subscribing to the leapmotion/data topic
def listener():
    rospy.init_node('leap_sub', anonymous=True)
    rospy.Subscriber("leapmotion/data", leapros, callback)
    rospy.spin()
#talker module for publishing the linear and angular data into a topic which the node controlling the robot can subscribe to
def talker(vel, omg):
    pub = rospy.Publisher('leap_chatter', Vector3, queue_size=10)
    rate = rospy.Rate(0.001) 
    try : 
	tw = Vector3(vel,omg,0)
	pub.publish(tw)
	#rate.sleep()
    except	rospy.ROSInterruptException:
	pass
#main function
if __name__ == '__main__':
    listener()
