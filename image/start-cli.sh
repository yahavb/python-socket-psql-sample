#!/bin/bash -x

while true
do
  echo "ping" | netcat $PYTHON_SRV_SVC_SERVICE_HOST $PYTHON_SRV_SVC_SERVICE_PORT
  sleep 1
done
