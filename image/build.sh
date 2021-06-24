#!/bin/bash
  
#region="us-west-2"
version="latest"

region=$(cat config | grep region | awk -F\= '{print $2}'|sed 's/ //g')
account=$(aws sts get-caller-identity --output text --query Account)
repo="python-socket-psql-sample"
repo_url=$account'.dkr.ecr.'$region'.amazonaws.com/'$repo':'$version

aws cloudformation create-stack --stack-name $repo --template-body file://./ecr-repos.json

aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $repo_url
docker build -t $repo .
docker tag $repo:latest $repo_url
docker push $repo_url
