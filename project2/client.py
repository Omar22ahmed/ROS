#!/usr/bin/env python3
import rospy
from client_server.srv import mult , multRequest
import random
global num
global num1
global char
global char1

rospy.init_node('client')
client=rospy.ServiceProxy('Encryption_service',mult)
rospy.wait_for_service
request = multRequest()

name = "Omar Ahmed"
char_list = [char for char in name]
ascii_array = []
print("The original name is  ",name)

for char1 in char_list:
    # Convert the character to ASCII and append to the array
     ascii_value = ord(char1)
     ascii_array.append(ascii_value)

     

result_array = []
key= random.randint(1, 100)

for num in ascii_array:
    result_value = num ^ key
    result_array.append(result_value)

new_array=[]
for num1 in result_array:
    # Convert the character to ASCII and append to the array
     ascii_value = chr(num1)
     new_array.append(ascii_value)

word = ''.join(new_array)
print("new name",word)

request.key= key
request.encrypted=word
response = client(request)
print(response)
print("----------------------")

