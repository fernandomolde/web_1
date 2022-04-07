import os
from bottle import route,run,TEMPLATE_PATH,jinja2_view,static_file,request,redirect
import sqlite3

BASE_DATOS = os.path.join(os.path.dirname(__file__),'personas.db')

#Esto le indica a template como se llama la carpeta
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__),'templates'))

@route('/static/<filename:path>')    #Para implementar Css
def server_static(filename):         # el path lo que hace es que te muestre la imagen
    return static_file(filename,root='./static')

@route('/')
@jinja2_view('home.html') #Aqui le decimos como se llama el archivo
def hola():
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "select p.id ,p.nombre,p.apellidos,p.dni,to2.descripcion,tn.descripcion from persona p left join T_ocupacion to2 on p.id_ocupacion = to2.id LEFT join T_numero tn on tn.id=p.id_numero "
    cursor = cnx.execute(consulta)
    filas = cursor.fetchall() #Trae todas las filas para procesarlos
    cnx.close()
    return {"datos": filas}

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('formulario.html')
def mi_form(id=None):
    # Ocupaciones
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "select * from T_ocupacion"
    cursor = cnx.execute(consulta)
    ocupaciones = cursor.fetchall() # Obtiene todas las filas 

    # Números
    consulta = "select * from T_numero"
    cursor = cnx.execute(consulta)
    numeros = cursor.fetchall()

    #Vehiculos
    consulta = "select * from T_vehiculo"
    cursor = cnx.execute(consulta)
    vehiculos = cursor.fetchall()

    if id is None: # Estamos en un alta
        return {'ocupaciones':ocupaciones,'numeros':numeros, 'vehiculos':vehiculos}
    else:
        consulta = "select id,nombre,apellidos,dni,id_ocupacion,id_numero from persona where id = ?"
        cursor = cnx.execute(consulta,(id,)) #La coma despues del ID,dice que es una tupla
        filas = cursor.fetchone() # Obtiene 1 fila para procesarla

    #   Mis_vehiculos
    consulta = f"select id_vehiculo from persona_vh where id_persona = {id}"
    cursor = cnx.execute(consulta)
    tmp = cursor.fetchall()
    mis_vehiculos = []
    for t in tmp:
        mis_vehiculos.append(t[0])

    cnx.close()
    return {'datos':filas,'ocupaciones':ocupaciones,'numeros': numeros,'vehiculos':vehiculos,'mis_vehiculos':mis_vehiculos}

@route('/guardar', method='POST')
def guardar(): 
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni = request.POST.dni
    id = request.POST.id
    ocupacion = request.POST.ocupacion
    numero = request.POST.numero
    vehiculos = request.POST.dict['vehiculo'] # Esto es una lista vehiculos
    cnx = sqlite3.connect(BASE_DATOS)


    if id =='': #Alta

        consulta = "insert into persona(nombre, apellidos,dni,id_ocupacion,id_numero) values (?,?,?,?,?)"
        tmp = cnx.execute(consulta,(nombre,apellidos,dni,ocupacion,numero))
        nuevo_id = tmp.lastrowid # Para conseguir el ultimo id de la fila
        # ----------------------
        for v in vehiculos:
            nuevos_vh = f'insert into persona_vh(id_persona,id_vehiculo) values ({nuevo_id},{v})' # insertamos en la tabla personas_vh, 
            cnx.execute(nuevos_vh)                                                                # el id de persona y de vehiculo y de valor,nuevo id y v que lo hemos definido antes
    else: #Actualizacion
         
        consulta = "update persona set nombre = ?, apellidos = ?, dni =?, id_ocupacion=?, id_numero=? where id =?"
        cnx.execute(consulta,(nombre,apellidos,dni,ocupacion,numero,id))
        
        # Mis_vehiculos
        consulta = f'delete from persona_vh where id_persona = {id}'
        cnx.execute(consulta)
        # Se borra todos los vehiculos de una persona e inserto los nuevos
        #-----------------------------------------
        for v in vehiculos:
            nuevos_vh = f"""insert into persona_vh(id_persona,id_vehiculo) values({id},{v})"""
            cnx.execute(nuevos_vh)

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
        cnx.close()    # Codigo para borrar
    redirect('/')

run(host='localhost',port=8080,debug=True)