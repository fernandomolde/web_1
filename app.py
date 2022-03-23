import os
from bottle import route,run,TEMPLATE_PATH,jinja2_view,static_file
#esto le indica a template como se llama la carpeta
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__),'templates'))

@route('/static/<filename>')    #Para implementar Css
def server_static(filename):
    return static_file(filename,root='./static')

@route('/')
@jinja2_view('home.html') #Aqui le decimos como se llama el archivo
def hola():
    return {'datos':[
        ('Teo',1,'lunes'),
        ('Jose',2,'martes'),
        ('Pau',3,'Jueves')]}



run(host='localhost',port=8080,debug=True)