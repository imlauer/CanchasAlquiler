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


add_place(){
  curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"lugar_nombre":"Futbol 5","owner":"Roberto Diaz","bar":1,"preciodia":100,"precionoche":311,"incluye":"Dos cervezas","fotoperfil":"sdfs","fotoportada":"asdf","estacionamiento":1,"parrila":1,"telefono":"23131","correo_owner":"saf@asdf.com","ciudad":"posadas","provincia":"misiones","parrilla":1,"diadelasemana":2,"horaapertura_dia":65,"horacierre_dia"}' \
    http://localhost:5000/agregar_lugar
}

add_sport(){
  curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"lugar_id":1,"tipo_deporte":"tenis"}' \
    http://localhost:5000/agregar_deporte
}

# Ver tema de la fecha y hora comienzo
add_alquiler(){
  curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"id_lugar":1,"diadelasemana":2,"fechaalquiler":"2020-01-15","horacomienzo":438,"senado":150,"tiempo":3}' \
    http://localhost:5000/alquilar
}

agregar_horario(){
  curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"lugar_id":1,"diadelasemana":3,"horadeapertura_dia":420,"horadecierre_dia":720,"horadeapertura_tarde":900,"horadecierre_tarde":1200}' \
    http://localhost:5000/agregar/horario
}

me_gusta(){
  curl --header "Content-Type: application/json" \
    --request POST \
    http://localhost:5000/megusta/1
}

denunciar(){
  curl --header "Content-Type: application/json" \
    --request POST \
    http://localhost:5000/denunciar/1
}

reservas(){
  curl http://localhost:5000/misreservas
}


#register
#login
#secret_sin_token_de_acceso
#secret_
#usuarios
#logout_access
#add_place
#add_sport
#add_alquiler
#agregar_horario
reservas
