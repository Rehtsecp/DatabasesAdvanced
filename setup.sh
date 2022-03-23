#!/usr/bin/env bash

# Start MongoDB
sudo systemctl start mongod

# Start Redis
cd /redis-stable/src
redis-server
redis-cli ping

#Docker setup
#docker start dba_mong
#docker start dba_redis