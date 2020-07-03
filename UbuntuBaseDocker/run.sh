#!/bin/bash

docker stop potato_container;
docker rm potato_container;
docker run -d --name potato_container -p 8022:22 -p 8045:8045 -p 8081:8081 -v ~/.ssh/docker_keys:/docker_keys my/ubu &&
docker ps
