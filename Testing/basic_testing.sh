#!/bin/sh

# Login
login(){
  curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"nombre":"teassting","clave":"imlauer123"}' \
    http://localhost:5000/login
}

register(){
  curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"nombre":"RicardoLopez1","clave1":"imlauer123","clave2":"imlauer123","correo":"ricardoilopez@andressffds.ai","apodo":"Pruwba"}' \
    http://localhost:5000/registration
}

register
#login
