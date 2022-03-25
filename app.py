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

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('formulario.html')
def mi_form(id=None):
    if id is None:
        return {}
    else:
        cnx = sqlite3.connect(BASE_DATOS)
        consulta = "select id,nombre,apellidos,dni from persona where id = ?"
        cursor = cnx.execute(consulta,(id,)) #La coma despues del ID,dice que es una tupla
        filas = cursor.fetchone() # Obtiene 1 fila para procesarla
        cnx.close()

        return {'datos':filas}

@route('/guardar', method='POST')
def guardar(): 
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni = request.POST.dni
    id = request.POST.id
    cnx = sqlite3.connect(BASE_DATOS)


    if id =='': #Alta

        consulta = "insert into persona(nombre, apellidos,dni) values (?,?,?)"
        cnx.execute(consulta,(nombre,apellidos,dni,))

    else:#Actualizacion
         
        consulta = "update persona set nombre = ?, apellidos = ?, dni =? where id =?"
        cnx.execute(consulta,(nombre,apellidos,dni,id))
        
    cnx.commit()
    cnx.close()
    redirect('/') #Esto lo que hace que vuelve a la raiz



run(host='localhost',port=8080,debug=True)