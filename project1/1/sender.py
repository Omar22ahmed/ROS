#!/usr/bin/env python3

import rospy
import random
import math as m
from std_msgs.msg import Int16, Float32
import time

n = 0  # Variable to indicate if the correct data has been received
encrypted_num = 0  # Variable to store the encrypted number

def my_callback(data):
    global encrypted_num
    global n
    data_back = data.data
    rospy.loginfo("I received %i", data_back)
    if data_back == encrypted_num:
        rospy.loginfo("Received data == encrypted data")
        n = 1
    else:
        rospy.logwarn("Data received is incorrect")
        n = 0

if __name__ == 'main':
    rospy.init_node('Synchronous_Publisher', anonymous=True)
    pubb = rospy.Publisher('encrypted', Int16, queue_size=10)
    sub = rospy.Subscriber("dycrypted", Float32, my_callback)
    rate = rospy.Rate(0.5)
    
    while not rospy.is_shutdown():
        if n == 1:
            n = 0
            j = random.randint(1, 10)
            encrypted_num = (j ** 2 + 10)
            rospy.loginfo(encrypted_num)
            pubb.publish(encrypted_num)
            time.sleep(3)
        elif n == 0:
            rospy.loginfo ("No message received. Please send it again.")
            j = random.randint(1, 30)
            encrypted_num = (j**2 + 10)
            pubb.publish(encrypted_num)
            rate.sleep()