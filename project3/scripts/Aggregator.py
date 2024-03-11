#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32, String, Int32
from weather_monitoring.srv import monitor, monitorRequest  #Import the custom service and its request

#Intialize the global variables
temperature = None
pressure = None
humidity = None
prev_temp=0
prev_press=0
prev_h=0

#
##
### First it acts as a Subscriber
##
#

#Recieve the values from the on field sensonrs
def pose_callback(data: Float32, sensor_type: str):
    global temperature, pressure, humidity
    
    if data is not None:                            
        
        if sensor_type == 'temperature':              #Temperature data recieved
            temperature = data.data                   #Store the recieved value in 'temperature'
            check_pressdata()                         #Check for sensor fault        
        
        elif sensor_type == 'pressure':               #Pressure data recieved
            pressure = data.data                      #Store the recieved value in 'pressure'
            check_hdata()                             #Check for sensor fault
        
        elif sensor_type == 'humidity':               #Humidity data recieved
            humidity = data.data                      #Store the recieved value in 'humidity'
            check_tempdata()                          #Check for sensor fault
    
    if all([temperature, pressure, humidity]) or not any([temperature, pressure, humidity]):                                  #Shutdown or normal operation

        if all([temperature, pressure, humidity]):                                                                            #Normal operation: "All values recieved"
            rospy.loginfo(f"Temperature: %.2f, Pressure: %.2f, Humidity: %.2f", temperature, pressure, humidity)
            rospy.loginfo("New value recieved")
            call_service(temperature, pressure, humidity)
            
        else:                                                                                                                 #Shutdown case: Do nothing
            temperature = None
            pressure = None
            humidity = None

    else:                                                                                                                     #One or Two missing sensor data
        message = "Missing sensor data: temperature=%s, pressure=%s, humidity=%s" % (temperature, pressure, humidity)        
        rospy.logwarn(message)                        #Display a warning indication for fault 
        rospy.loginfo("New value recieved")


#Temperature sensor fault check
def check_tempdata():
    global temperature
    global prev_temp
    rospy.loginfo("checking tempreture data")

    if prev_temp == temperature:                           #Same reading for random values means latching
        message = "Fault at Tempreture sensor"             
        rospy.logwarn(message)                             #Display a warning about sensor fault
        temperature = None                                 #Set temperature to a fault indicator     
        check_pressdata()
    else:
        prev_temp = temperature                            #Store it to check the next value
        
    return(temperature)

#Pressure sensor fault check
def check_pressdata():
    global pressure
    global prev_press
    rospy.loginfo("checking Pressure data")
        
    if prev_press == pressure:                             #Same reading for random values means latching
        message = "Fault at Pressure sensor"
        rospy.logwarn(message)                             #Display a warning about sensor fault
        pressure = None                                    #Set pressure to a fault indicator         
        check_hdata()
    else:
        prev_press = pressure                              #Store it to check the next value

    return(humidity)

#Humidity sensor fault check
def check_hdata():
    global humidity
    global prev_h
    rospy.loginfo("checking humidity data")
    if prev_h == humidity:                                  #Same reading for random values means latching
        message = "Fault at Humidity sensor"
        rospy.logwarn(message)                              #Display a warning about sensor fault
        humidity = None                                     #Set humidity to a fault indicator 
        check_tempdata
    else:
        prev_h = humidity                                   #Store it to check the next value

    return(humidity)


#
##
### Second it acts as a Client
##
#


def call_service(temp: float, pressure: float, humidity: float):
    try:
        rospy.wait_for_service('monitor')                              #Synchronous connection with the server with custom service "monitor" rules
        aggregator = rospy.ServiceProxy('monitor', monitor)            #
        request = monitorRequest()                                     #Define a cutom request with the detected types
        #store the request parameters in values
        request.temperature = temp
        request.pressure = pressure
        request.humidity = humidity

        response = aggregator(request)                                 #Asking for a response for this request
        print(response)
        print("Monitoring successful.")                                #Three values recieved & Three values sent
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")


#The main function
if __name__ == '__main__':
    rospy.init_node("Aggregator", anonymous=True)                                                       #Intialize the aggregator node
    rospy.Subscriber('On-fields/temperature', Float32, pose_callback, callback_args='temperature')      #Subscribe from the temperature topic
    rospy.Subscriber('On-fields/pressure', Float32, pose_callback, callback_args='pressure')            #Subscribe from the pressure topic
    rospy.Subscriber('On-fields/humidity', Float32, pose_callback, callback_args='humidity')            #Subscribe from the humidity topic
    rospy.loginfo("Aggregator started monitoring")                                                      #Display an indication                 
    rospy.spin()