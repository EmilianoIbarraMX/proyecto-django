from django.shortcuts import render
from .models import Alumnos
from .forms import ComentarioContactoForm
from .models import ComentarioContacto
from django.shortcuts import get_object_or_404
import datetime

# Create your views here.

def registros(request):
    alumnos=Alumnos.objects.all()
    return render(request, 'Registros/principal.html',{'9B':alumnos})

def registrar(request):
    if request.method == "POST":
        form = ComentarioContactoForm(request.POST)
        if form.is_valid():
            form.save()
            comentarios=ComentarioContacto.objects.all()
            return render(request,'registros/comentarios.html',{'comentario':ComentarioContacto})
    form = ComentarioContactoForm()
    return render(request,'registros/contacto.html',{'form' : form })

def contacto(request):
    return render(request,'registros/contacto.html')
#Indicamos el lugar en donde se renderiza el resultado de esta vista

def comentarios(request):
    comentario=ComentarioContacto.objects.all()
    return render(request,'registros/comentarios.html',{'comentarios':comentario})

def eliminarComentario(request, id,
    confimracion='registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method=='POST':
        comentario.delete()
        comentarios=ComentarioContacto.objects.all()
        return render(request,"registros/comentarios.html",{'comentarios':comentarios})
    return render(request,confimracion,{'object':comentario})


def consultarComentarioIndividual(request,id):
    comentario=ComentarioContacto.objects.get(id=id)
    return render(request,"registros/editar.html",{'comentario':comentario})

def editarComentarioContacto(request,id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form =ComentarioContactoForm(request.POST, instance=comentario)
    if form.is_valid(): #Si los datos recibidos son correctos
        form.save()
        comentarios=ComentarioContacto.objects.all()
        return render(request,"registros/editar.html",{'comentario':comentario})
    return render(request,"registros/comentarios.html",{'comentarios':comentarios})

def consultar1(request):
#con una sola condicion
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
#con una sola condicion
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
#Si solo deseamos recuperar ciertos datos agregados la #funcion only,
#listando los cmpos que queremos obtener de la #consulta empleada filter()
#o en el ejemplo all()
    alumnos=Alumnos.objects.all().only("matricula","nombre","carrera","turno","imagen")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
#con una sola condicion
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
#con una sola condicion
    alumnos=Alumnos.objects.filter(nombre__in=["Juan","Ana"])
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar6(request):
#con una sola condicion
    fechaInicio = datetime.date(2024,7,1)
    fechaFin = datetime.date(2024,7,15)
    alumnos=Alumnos.objects.filter(crated__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
#Consultando entre modelos
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultasSQL(request):
    alumnos=Alumnos.objects.raw('SELECT id, matricula, nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})