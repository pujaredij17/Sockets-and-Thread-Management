from tkinter import *
import socket
import threading
import time
from tkinter import scrolledtext
from datetime import datetime
import datetime
from email.utils import formatdate, localtime
import os

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
    return http_format

def connect_client():
    
    try:
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() #Get local machine name
        port = 12345                # Reserve a port for your service.
        s.bind((host, port))        # Bind to the port
        
    except socket.error:
        print("Socket Error")   
    
    s.listen(3)                 # Now wait for client connection.

    threading.Thread(target = listenToClient,args = (s,)).start()

def listenToClient(s):    
        
    while True:
            
        c, addr = s.accept()
        #print("connection successful with " , addr)
        #c.send(b'connected to server')
        c.send(get_http_message("connected to server\n").encode())
#         print(c.recv(1024))
         
        msg = c.recv(1024)
        msg = parse_http_message(msg)
        
        T.insert(END, 'Connected to ' + msg + '\n')
        
        threading.Thread(target = communicate,args = (c,msg,)).start()

def communicate(c,msg):        
    
    while True:
        
        try:            
            
            recv_random_num = c.recv(1024) 
            
            if not recv_random_num:
                T.insert(END, msg + ' disconnected the session\n')  

                
            recv_random_num = parse_http_message(recv_random_num)
            
            T.insert(END, 'Server waiting ' + recv_random_num + ' seconds for ' + msg + '\n')
            time.sleep(int(recv_random_num))
            
            msg1 = ('Server waited ' + recv_random_num + ' seconds for ' + msg + '\n\n')
            
            c.send(get_http_message(msg1).encode())
            T.insert(END, msg1)
        
        except RuntimeError:
             
            print('server error')
            os._exit(0)  
             

        except:
            T.insert(END, msg + ' disconnected the session\n')  
            c.close()  
            break
                
    
 

r=Tk()
r.title('Server')

button = Button(r, text='start', width=25, command=connect_client) 
button.pack()
 
T = scrolledtext.ScrolledText(r)
T.pack()
  
r.mainloop()