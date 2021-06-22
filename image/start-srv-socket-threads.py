#!/usr/bin/python3

import socket
import threading
import pg8000.native
import os
import time
import logging
import boto3
import base64
import json
from botocore.exceptions import ClientError


HOST = '0.0.0.0'  
PORT = int(os.environ.get('SRV_PORT'))
DBHOST=os.environ.get('DBHOST')
TCP_BUFF_SIZE=int(os.environ.get('TCP_BUFF_SIZE'))
SECRET_NAME = os.environ.get('DBSECRET')
REGION_NAME = os.environ.get('REGION')

session = boto3.session.Session()
client = session.client(
  service_name='secretsmanager',
  region_name=REGION_NAME
)
secret = client.get_secret_value(
         SecretId=SECRET_NAME
)
secret_dict = json.loads(secret['SecretString'])
username = secret_dict['username']
passw = secret_dict['password']

dbconn=pg8000.connect(
        username,
        host = DBHOST,
        password = passw
    )

def get_transaction():
  print('get_transaction',flush=True)
  for row in dbconn.run("select id from pythonsocketpsqlsample limit 10"):
    print('transaction from db is {}'.format(row),flush=True)

def thread_handler(request):
  print('thread_handler.run():{}'.format(request),flush=True) 
  trsid=get_transaction()
  #conn.sendall(str.encode('thread_handler.run():'+str(request)+' db trs:'+get_transaction()))
  conn.sendall(str.encode('thread_handler.run():'+str(request)+' db trs:get_transaction()'))


if __name__ == '__main__':
  print('server starts',flush=True)
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('server listen on {}:{}'.format(HOST,PORT),flush=True)
    while True:
      conn, addr = s.accept()
      with conn:
        print('Connected by {}'.format(addr),flush=True)
        while True:
            request = conn.recv(TCP_BUFF_SIZE)
            if not request:
                break
            req_thread = threading.Thread(target=thread_handler,args=(request,))
            req_thread.start()
    s.close() 
