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
    --data '{"nombre":"Acer_","clave1":"acer13","clave2":"acer13","correo":"acer_@gmail.com","apodo":"sad"}' \
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
    -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzgwOTY2OTYsIm5iZiI6MTU3ODA5NjY5NiwianRpIjoiMjJiZTVhMTctNjdiZi00NzE1LWExNjUtMWQxMDA4NDkwMGM2IiwiZXhwIjoxNTc4MDk3NTk2LCJpZGVudGl0eSI6IkFjZXJfIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.WPvMIlT16qy4GjMsj2LmOqkG0wx-dGa-yBOpZl9ePUc" \
    http://localhost:5000/secret
}

usuarios(){
  curl --header "Content-Type: application/json" \
    http://localhost:5000/lista_usuarios
}

logout_access(){
  curl --header "Content-Type: application/json" \
    --request GET \
    -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzgwOTY2OTYsIm5iZiI6MTU3ODA5NjY5NiwianRpIjoiMjJiZTVhMTctNjdiZi00NzE1LWExNjUtMWQxMDA4NDkwMGM2IiwiZXhwIjoxNTc4MDk3NTk2LCJpZGVudGl0eSI6IkFjZXJfIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.WPvMIlT16qy4GjMsj2LmOqkG0wx-dGa-yBOpZl9ePUc" \
    "http://localhost:5000/logout/access"
}

logout_refresh(){
  curl --header "Content-Type: application/json" \
    "http://localhost:5000/logout/refresh"
}
token_refresh(){
  curl --header "Content-Type: application/json" \
    "http://localhost:5000/token/refresh"
}



# faltan /logout/acess, /logout/refresh, /token/refresh, 





#register
#login
#secret_sin_token_de_acceso
#secret_
#usuarios
logout_access
