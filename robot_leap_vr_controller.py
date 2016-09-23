#!/usr/bin/env python
#author rohan, vishweshwaran 
#ROS Node for position control of robot based on head orientation data from android application 
#(and velocity information from leap motion sensor )
# Preprocessor required 
#importing libraries
import rospy
import rospy
from geometry_msgs.msg import Vector3, Twist
import socket   
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *
from tf.msg import *
import math
import tf

# Global variables to be initialized here
pos = 0;
pos_init = 0;
sock = 0;
yaw_degrees =0;
count = 0;
flag =0;
omega =0;
mutex = 0;
currstate =1;
prevstate =1;
v=0;
ang=0;
Calibrate_Complete=0;
Init_Flag=0;
# Global variables declaration ends here

# Code for Callback starts here 
def callback(data):
    global sock
    global currstate
    global v
    global ang
    print(data.x)
    #obtain linear velocity data from leap motion sensor
    v=float(data.x)/100.0
    # Connection is made with VR app 	
    connection,client_address=sock.accept()
    # Obtain angular data from VR app
    ang = float(connection.recv(10))
    # Source data in opposite convention
    ang = 360-ang 
    currstate = 1
    return 0
# Code for Callback ends here

# Code for publisher starts here 
def publisher (v1,ang1): 
    global pos
    global pos_init
    global omega
    global flag
    global currstate
    # Calculating the angular velocity
    delta = pos-ang1;
    #using on-off controller for tracking user
    #stop if the error lies within the threshold
    if (abs(pos-ang1)<=10):
	omega = 0;dpos =0;
    #rotate clockwise to follow user
    elif (pos > ang1):
	omega = -0.1;
    #rotate anti-clockwise to follow user
    elif(pos < ang1):
	omega = 0.1;
    #finding the shortest route
    if (abs(delta)>=180):
	omega = -1*omega
    # publishing the linear velocity and angular velocity
    pub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=1)
    try : 
	tw = Twist(Vector3(v1,0,0), Vector3(0,0,omega))
	pub.publish(tw)
    	currstate = 0;
    except  rospy.ROSInterruptException:
	pass
    currstate = 0;
    return 0
# Code for publisher ends here

# Code for listener starts here
def listener():
    global sock
    rospy.Subscriber('leap_chatter', Vector3, callback, queue_size=1)
# Code for listener ends here

# Code for Position starts here
#callback for retreiving odometry data from robot for feedback
def Position(odom_data):
    global yaw_degrees
    global pos_init
    global count
    global flag 
    global pos
    global currstate
    global Calibrate_Complete
    global v
    global ang
    flag = 0;
    # Calculating euler angles from the orientation of the robot in quaternion as feedback from the robot  
    quaternion = odom_data.pose.pose.orientation
    x = quaternion.x
    y = quaternion.y
    z = quaternion.z
    w = quaternion.w
    quaternion1 = (x,y,z,w)
    euler = tf.transformations.euler_from_quaternion(quaternion1)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    yaw_degrees=math.degrees(yaw)
    if(yaw_degrees <0):
	yaw_degrees = yaw_degrees+360;
    if(Calibrate_Complete == 0):
	pos_init = yaw_degrees
	currstate = 0;
    else:
	pos = yaw_degrees
	pos =pos-pos_init;
    	if(pos <0):
		pos = pos+360;
        if (currstate ==1):
		currstate = 2
    Calibrate_Complete = 1;
# Code for position ends here 

# Code for Calibrate starts here
def calibrate():   
     rospy.Subscriber('/RosAria/pose',Odometry,Position)
# Code for Calibrate ends here

# State Machine for the program starts here
if __name__ == "__main__":
       global Init_Flag
       server_address=('10.0.1.25',9000)
       sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sock.bind(server_address)
       sock.listen(10)
       #calibrate robot on startup
       if(Init_Flag == 0):
       		rospy.init_node('listener', anonymous=True)
       		calibrate()
		Init_Flag = 1;

       while not rospy.is_shutdown():
        if(Calibrate_Complete == 1):
		if(currstate != prevstate):
			
			prevstate = currstate;
			if(currstate == 0):
			        #get velocity data from leap motion and orientation data from google VR
       				listener();
			elif(currstate == 1):
			        #get odometry data from P3DX robot
    				rospy.Subscriber('/RosAria/pose',Odometry,Position)
			elif(currstate == 2):
			        #publish data to the /RosAria/cmd_vel topic to control the robot with the desired control input
    				publisher(v,ang);
	# While ends here
# State Machine ends here
