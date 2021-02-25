import socket
import threading
import os
import sys
from collections import defaultdict

#locate the path where ip.txt is situated
file=open('C:\ip.txt','r')
lines=file.readlines()

#maintain count to reach till the line where ip is located
count=1
ip=""
for l in lines:
    if count==96:
        ip=l[39:52]
        break
    else:
        count+=1

print("IP is : ")
print(ip)
