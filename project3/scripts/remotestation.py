#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32, String
from weather_monitoring.srv import monitor, monitorResponse

def monitor_callback(request):
    
    response=monitorResponse()
#check for the values of data recieved to be within the suitable range and print indications
    
    if 10.0 <= request.temperature <= 100.0:
        response.Tvalidate = True                                                      
        print("Accepted temperature value: ", request.temperature)                    
    else:
        response.Tvalidate = False
        Terror = "Out of range reading: temperature=%s" % (request.temperature)
        rospy.logwarn(Terror)
        

    if 0.95 <= request.pressure <= 1.2:
        response.Pvalidate = True
        print("Accepted pressure value: ", request.pressure)
    else:
        response.Pvalidate = False
        Perror = "Out of range reading: pressure=%s" % (request.pressure)
        rospy.logwarn(Perror)


    if 0.7 <= request.humidity <= 0.95:
        response.Hvalidate = True
        print("Accepted humidity value: ", request.humidity)
    else:
        response.Hvalidate = False
        Herror = "Out of range reading:humidity=%s" % (request.humidity)
        rospy.logwarn(Herror)
    
    print("--------------------------------------------------------------")
    print(request)
    return response
    

rospy.init_node('remotestation')                                                          #Intialize the node named remotestation
rospy.Service('monitor', monitor, monitor_callback)                                       #Recieve requests as the custom service 
rospy.spin()
       
        