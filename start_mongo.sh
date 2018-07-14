#!/bin/bash
docker run -d -p 27017:27017 -v `pwd`/mongo-data:/data/db --name mongodb 'mongo:4.0'
