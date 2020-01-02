#!/bin/sh

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"clave":"xyz"}' \
  http://localhost:5000/login
