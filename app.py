import os
from bottle import route,run,TEMPLATE_PATH,jinja2_view,static_file,request,redirect
import sqlite3

BASE_DATOS = os.path.join(os.path.dirname(__file__),'personas.db')

#esto le indica a template como se llama la carpeta
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__),'templates'))

@route('/static/<filename>')    #Para implementar Css
def server_static(filename):
    return static_file(filename,root='./static')

@route('/')
@jinja2_view('home.html') #Aqui le decimos como se llama el archivo
def hola():
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "select id,nombre,apellidos,dni from persona"

    cursor = cnx.execute(consulta)
    filas = cursor.fetchall() #Trae todas las filas para procesarlos
    cnx.close()
    return {"datos": filas}

@route('/formulario')
@jinja2_view('formulario.html')
def mi_form():
    return {}

@route('/guardar', method='POST')
def guardar(): 
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni = request.POST.dni
     
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "insert into persona(nombre,apellidos,dni) values (?,?,?)"
    cnx.execute(consulta,(nombre,apellidos,dni))
    cnx.commit()
    cnx.close()
    redirect('/') #Esto lo que hace que vuelve a la raiz



run(host='localhost',port=8080,debug=True)