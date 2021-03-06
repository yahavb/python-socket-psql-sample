#!/usr/bin/python3

import socket
import socketserver
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

class Handler(socketserver.BaseRequestHandler):
  def handle(self):
    #while True:
      print('Handler thread_handler.run()',flush=True) 
      self.data=self.request.recv(TCP_BUFF_SIZE).strip()
      print('Handler thread_handler-data={}'.format(self.data),flush=True)
      get_transaction()
      self.request.sendall(self.data.upper())


if __name__ == '__main__':
  print('server starts',flush=True)
  server = socketserver.TCPServer((HOST, PORT), Handler)
  print('server listen on {}:{}'.format(HOST,PORT),flush=True)
  server.serve_forever()
