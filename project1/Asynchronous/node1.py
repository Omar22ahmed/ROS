#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
import random
num1=0
encrypted_data=0
decrypted_num=0
def waiting(encrypted_num):  #wait to check the encrypted number before sending a new number
    global encrypted_data
    rospy.loginfo('Hello')
    pub = rospy.Publisher('chatter',Int32,queue_size=10) 
    rate=rospy.Rate(3)
    rate.sleep()#As there is not enough time between creating the publisher and sending the message on it  for any listener node to register with this new publisher

    sub = rospy.Subscriber('Decrypted_topic',Int32,callback=pose_callback) 
    pub.publish(encrypted_num)
    
    
    rospy.spin() #to make the function wait untill a new message send by core function

def pose_callback(data): # Function to compare decrypted number with the random number
    global decrypted_num
    global num1
    decrypted_num=  data.data 
    rospy.loginfo("Recieved %d", decrypted_num)
    if (decrypted_num==num1):
        rospy.loginfo("correct")
        core() # to generate a new encrypted number and send it
    else :
        rospy.loginfo("fault")
        waiting()
        
def core():
    i=0
    i=i+1
    rospy.loginfo(i) 

    rospy.init_node("master",anonymous=True) #node initialization
    rospy.loginfo("generating") 
    global num1
    num1 = random.randint(1,100) # generating random number
    encrypted_num = num1 ** 2 + 10 #Encrytption equation
    rospy.loginfo("your encrypted number is %d", encrypted_num)
    waiting(encrypted_num) #sending encrypted number to waiting function 
if __name__ == '__main__':
        core()
    

   