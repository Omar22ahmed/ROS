#!/usr/bin/env python3
import rospy
from client_server.srv import mult , multResponse
global num
global num1
global char
global char2

def callback(msg):
			respond=multResponse()
			name=msg.encrypted
			char_list = [char for char in name]

			
			ascii_array = []

			for char2 in char_list:
					# Convert the character to ASCII and append to the array
					ascii_value = ord(char2)
					ascii_array.append(ascii_value)

			result_array = []
			key=msg.key
			for num in ascii_array:
					result_value = num ^ key
					result_array.append(result_value)

			new_array=[]
			for num1 in result_array:
					# Convert the character to ASCII and append to the array
					ascii_value = chr(num1)
					new_array.append(ascii_value)

			word = ''.join(new_array)
			respond.decrypted= word
			return respond

        
        

rospy.init_node('Server')
rospy.Service('Encryption_service',mult,callback)
rospy.spin()