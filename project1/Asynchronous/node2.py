#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
import random
def pose_callback(data):
    decrypted_num =  (data.data - 10) ** 0.5 #Decryption equation 
    rospy.loginfo("Recieved %d and it means %d",data.data , decrypted_num)

    pub=rospy.Publisher('Decrypted_topic', Int32 ,queue_size=10)
    rate=rospy.Rate(3)
    rate.sleep()
    pub.publish(int(decrypted_num)) #sending the decrypted number to be compared with the original number
    rospy.loginfo("Your decrypted number has been sent")


   


def core():
    rospy.init_node("slave",anonymous=True)
    rospy.loginfo("start")
    rospy.Subscriber('chatter',Int32,callback=pose_callback)
    rospy.spin()
if __name__ == '__main__':
    try :
        core()
    except rospy.ROSInternalException:
        pass