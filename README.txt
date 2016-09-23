=========================================================================================================================================
REAL-TIME GESTURE CONTROLLED ROBOT USING VIRTUAL REALITY
Authors: Rohan Sarkar, Ambujan Sothinathan, Vishveswaran Jothi, Dwarakanath Reddy
=========================================================================================================================================
Folder 1:
(1)PIVRStream.rar         - Contains the source code of the android application that streams raspberry pi video for google cardboard 
                            and sends head orientation information for the user
=========================================================================================================================================
Folder 2:
Leap_sensor_interface     - Contains the files required for interfacing with the leap motion and gesture recognition			
The Folder 2 contains the following 3 files:
(1)leap_gesture.py        - ROS Node to identify gestures,count fingers and measure hand palm position and orientation
(2)leap_sender.py         - ROS Node to publish the finger joint/palm position and orientation into the topic leapmotion/data (leapros message)
(3)leap_interface.py      - ROS Node provided by LeapSDK to interface with the Leap Motion Sensor
=========================================================================================================================================
Folder 3:
Robot_interface                - Contains the files required for interfacing with the robot
The Folder 3 contains the following 2 files: 
(1)robot_leap_controller.py    - ROS node to control the robot by using linear and angular velocities from the leap motion sensor
(2)robot_leap_vr_controller.py - ROS Node for position control of robot based on head orientation data from android application 
				 (and velocity information from leap motion sensor )
=========================================================================================================================================
Folder 4:
Leap_Sensor_ROS_Package        - Contains the entire ROS package for leap_motion_sensor
Note: Folder 2 and Folder 3 are a part of this package (/Leap_Sensor_ROS_Package/scripts/leap_sensor)
Note: For running this package various other ROS packages need to be installed (LeapSDK,leap_motion,RosAria)
=========================================================================================================================================
