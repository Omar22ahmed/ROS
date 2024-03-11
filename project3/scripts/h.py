#!/usr/bin/env python3
import rospy
import random
from std_msgs.msg import Float32

def speaker():
  rospy.init_node('Humidity', anonymous=True)
  pub = rospy.Publisher('On-fields/humidity', Float32, queue_size=10)
  rate = rospy.Rate(0.2)  # Publish at 0.2 Hz
  rospy.loginfo("Started publishing humidity")
  humidity=None

  while not rospy.is_shutdown():
      H = random.uniform(0, 2) 
      humidity = H
      rospy.loginfo("Humidity = %f", H)
      pub.publish(H)
      rate.sleep()

if __name__ == '__main__':
  try:
    speaker()
  except rospy.ROSInternalException:
    pass
