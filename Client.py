from tkinter import *
from tkinter import scrolledtext
import socket
import threading
import random
from datetime import datetime
import datetime
from email.utils import formatdate, localtime
import os
import time

def parse_http_message(message): # parse HTTP message
    data = message.decode().split('\r\n')[-1]
    data = data.replace('DATA:', '')
    return data

    
def get_http_message(message): # encode HTTP message
    http_format = 'POST /test HTTP/1.1\r\n'\
'Host: localhost\r\n'\
'Date: #DATE#\r\n'\
'User-Agent: client_application\r\n'\
'Content-Type: application/x-www-form-urlencoded\r\n'\
'Content-Length: #LEN#\r\n'\
'\r\n'\
'DATA:' + message
    http_format = http_format.replace('#LEN#', str(len(message)))
    date = formatdate(timeval=None, localtime=False, usegmt=True)
    http_format = http_format.replace('#DATE#', date)
    return http_format

def connect_server():
    
    s= socket.socket()
    host = socket.gethostname()
    port = 12345
    
    s.connect((host,port))
#     s.send(b'Client1')

    msg = s.recv(1024)
    msg = parse_http_message(msg)

    
    T.insert(END,msg)
    
#     print(e1.get()) 
    s.send(get_http_message(e1.get()).encode())  
    
    
    threading.Thread(target = send_random,args = (s,)).start()

def send_random(s):
    
    while True:
        
        try:
        
            random_num = random.randint(5,15)
            T.insert(END, '\n')
            T.insert(END, 'Server waiting for ' + str(random_num) + '\n')
            
            random_num = str(random_num)
            
            s.send(get_http_message(random_num).encode())
            
    
            msg1 = s.recv(1024)\
            
            if not msg1:
                T.insert(END, 'Server disconnected the session')    
            
            msg1 = parse_http_message(msg1)
            T.insert(END, msg1)
        
        except RuntimeError:
            print('Client Error')  
            os._exit(0)  
           
             
        except:
            
            T.insert(END, 'Server disconnected the session')             
            s.close()
            os._exit(0)  
             
    T.insert(END, 'Server disconnected the session')             


def quit():
    
#     send(get_http_message(e1.get()).encode()) 
    T.insert(END, 'disconnecting the session')    
    os._exit(0)   

         

r = Tk()
r.title('Client1')

button1 = Button(r,text='connect', width=25,command=connect_server)
button1.grid(row=0,column=2)

button2 = Button(r,text='quit', width=25,command=quit)
button2.grid(row=5,column=2)

T = scrolledtext.ScrolledText(r)
T.grid(row=2)

Label(r, text='Client Name').grid(row=0,column=0) 
e1 = Entry(r) 
e1.grid(row=0, column=1) 

r.mainloop()


