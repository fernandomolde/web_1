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
    consulta = "select id,nombre,apellidos,dni,id_ocupacion from persona"

    cursor = cnx.execute(consulta)
    filas = cursor.fetchall() #Trae todas las filas para procesarlos
    cnx.close()
    return {"datos": filas}

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('formulario.html')
def mi_form(id=None):
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "select * from T_ocupacion"
    cursor = cnx.execute(consulta)
    ocupaciones = cursor.fetchall() # Obtiene todas las filas 

    if id is None:
        return {'ocupaciones':ocupaciones}
    else:
        consulta = "select id,nombre,apellidos,dni from persona where id = ?"
        cursor = cnx.execute(consulta,(id,)) #La coma despues del ID,dice que es una tupla
        filas = cursor.fetchone() # Obtiene 1 fila para procesarla

    cnx.close()
    return {'datos':filas,'ocupaciones':ocupaciones}

@route('/guardar', method='POST')
def guardar(): 
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni = request.POST.dni
    id = request.POST.id
    ocupacion = request.POST.ocupacion
    cnx = sqlite3.connect(BASE_DATOS)


    if id =='': #Alta

        consulta = "insert into persona(nombre, apellidos,dni,id_ocupacion) values (?,?,?,?)"
        cnx.execute(consulta,(nombre,apellidos,dni,ocupacion))

    else:#Actualizacion
         
        consulta = "update persona set nombre = ?, apellidos = ?, dni =?, id_ocupacion=? where id =?"
        cnx.execute(consulta,(nombre,apellidos,dni,ocupacion,id))
        
    cnx.commit()
    cnx.close()
    redirect('/') #Esto lo que hace que vuelve a la raiz

@route('/borrar/<id:int>')
def borrar(id=None):
    if id is None:
        return {}
    else:
        cnx = sqlite3.connect(BASE_DATOS)
        consulta = "DELETE FROM persona where id = " + str(id)
        # consulta = f'delete from persona where id ="{id}"'
        cnx.execute(consulta)
        cnx.commit()
        cnx.close()                     # Codigo para borrar
    redirect('/')

run(host='localhost',port=8080,debug=True)