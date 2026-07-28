#!/bin/bash

docker pull quay.io/uvelyster/mysql:5.7
docker tag quay.io/uvelyster/mysql:5.7 mysql

docker network create myappnet

docker run -d --name dbsvc --network myappnet -e MYSQL_DATABASE=webtest -e MYSQL_ROOT_PASSWORD=Test123! -v ./sql:/docker-entrypoint-initdb.d -p 3306:3306 mysql
