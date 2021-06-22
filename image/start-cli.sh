#!/bin/bash -x

while true
do
  echo $TCPCMD | netcat $PYTHON_SRV_SVC_SERVICE_HOST $PYTHON_SRV_SVC_SERVICE_PORT
  sleep 5
done
