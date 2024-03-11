#!/usr/bin/env python3
import rospy
import random
from std_msgs.msg import Float32

def speaker():
  rospy.init_node('Temperature', anonymous=True)
  pub = rospy.Publisher('On-fields/temperature', Float32, queue_size=10)
  rate = rospy.Rate(0.2)  # Publish at 0.2 Hz
  rospy.loginfo("Started publishing temperature")
  temperature=None
  
  while not rospy.is_shutdown():
      T = random.uniform(0, 130)  # Generate temperature between 0 and 130
      temperature = T
      rospy.loginfo("Temperature = %f", T)
      pub.publish(T)
      rate.sleep()
  
   
if __name__ == '__main__':
  try:
    speaker()
  except rospy.ROSInternalException:
    pass

