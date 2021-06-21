#!/usr/bin/python3

import socket
import threading
import pg8000.native
import os
import time
import logging

HOST = '0.0.0.0'  
PORT = int(os.environ.get('SRV_PORT'))
DBHOST=os.environ.get('DBHOST')
TCP_BUFF_SIZE=int(os.environ.get('TCP_BUFF_SIZE'))

dbconn=pg8000.connect(
        "postgres",
        host = DBHOST,
        password = "Admin1234!"
    )

def get_transaction():
  print('get_transaction')
  for row in dbconn.run("select id from pythonsocketpsqlsample limit 10"):
    print('transaction from db is {}'.format(row))

def thread_handler(request):
  print('thread_handler.run():{}'.format(request)) 
  trsid=get_transaction()
  #conn.sendall(str.encode('thread_handler.run():'+str(request)+' db trs:'+get_transaction()))
  conn.sendall(str.encode('thread_handler.run():'+str(request)+' db trs:get_transaction()'))


if __name__ == '__main__':
  print('server starts')
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('server listen on {}:{}'.format(HOST,PORT)) 
    conn, addr = s.accept()
    with conn:
        print('Connected by {}'.format(addr))
        while True:
            request = conn.recv(TCP_BUFF_SIZE)
            if not request:
                break
            req_thread = threading.Thread(target=thread_handler,args=(request,))
            req_thread.start()
