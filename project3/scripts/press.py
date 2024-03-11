#!/usr/bin/env python3
import rospy
import random
from std_msgs.msg import Float32

def speaker():
  rospy.init_node('Pressure', anonymous=True)
  pub = rospy.Publisher('On-fields/pressure', Float32, queue_size=10)
  rate = rospy.Rate(0.2)  # Publish at 0.2 Hz
  rospy.loginfo("Started publishing pressure")
  pressure=None 

  while not rospy.is_shutdown():
      P = random.uniform(0, 3)  # Generate pressure between 0 and 1.5
      pressure = P
      rospy.loginfo("Pressure = %f", P)
      pub.publish(P)
      rate.sleep()

if __name__ == '__main__':
  try:
    speaker()
  except rospy.ROSInternalException:
    pass

