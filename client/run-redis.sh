#!/bin/sh
docker run -d --name avala-client-redis -p 6379:6379 --restart always redis
