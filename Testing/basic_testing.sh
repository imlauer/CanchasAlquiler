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
    --data '{"nombre":"Silence","clave1":"imlauer123","clave2":"imlauer123","correo":"silence@andres.ai","apodo":"ssad"}' \
    http://localhost:5000/registration
}

secret_sin_token_de_acceso(){
  curl --header "Content-Type: application/json" \
    --request GET \
    http://localhost:5000/secret
}

secret_(){
  curl --header "Content-Type: application/json" \
    --request GET \
    -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Nzc5OTQ0ODAsIm5iZiI6MTU3Nzk5NDQ4MCwianRpIjoiZTQ3NmU5YzEtYWQ5Yy00NGVjLWIzYmQtZjc3NGFkMWU5YmIxIiwiZXhwIjoxNTc3OTk1MzgwLCJpZGVudGl0eSI6IkltbGF1ZXJBbmRyZXciLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.M3bwk2IPh_CgEhHTT4IB_dNJtauzIK_qDKJRcARgHOE" \
    http://localhost:5000/secret
}

usuarios(){
  curl --header "Content-Type: application/json" \
    --request GET \
    http://localhost:5000/lista_usuarios
}





#register
#login
#secret_sin_token_de_acceso
#secret_
usuarios
