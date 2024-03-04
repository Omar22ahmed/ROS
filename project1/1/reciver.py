#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32      #to enable recieving integer via channel

#callback function to be excuted after recieving message via channel
def pose_callback(data):
    decrypted_num =  (data.data - 10) ** 0.5 
    rospy.loginfo("Recieved %d and it means %d",data.data , decrypted_num) #print recieved number and the corresponding decrypted number


if __name__ == '__main__':
    rospy.init_node("listener",anonymous=True)
    rospy.Subscriber('chatter',Int32,callback=pose_callback)   #declare at which topic will recieve messages
    rospy.loginfo("Node has been started")
    rospy.spin()  #keeps the node excuting untill the node has been killed