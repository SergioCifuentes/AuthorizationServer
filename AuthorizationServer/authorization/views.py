from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .models import *
from datetime import datetime, date
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from django.views import View
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def signin(request):

    context = {}
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:

            auth.login(request, user)
            return redirect('/authorization/home')
        else:

            messages.error(request, 'invalid username or password')
            return redirect("/authorization/signin")

    else:

        return render(request, "login.html", context)


def home(request):
    if request.method == 'POST':
        print("POST")
        estado = request.POST['estados']
        nuevo_estado = Estado_Servidor(estado=estado, fecha=datetime.now())
        nuevo_estado.save()
        return redirect('/authorization/home')
    else:
        context = {'estado': Estado_Servidor.objects.order_by('-fecha').first()
                   }
        return render(request, "home.html", context)

def reportes(request):
    if request.method == 'POST':
        pass
    else:
        context = {'Transacciones': Transaccion_Autorizado.objects.all()
                   }
        return render(request, "reportes.html", context)

class EstadoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Estado_Servidor.objects.order_by('-fecha')
    serializer_class = EstadoSerializer
    permission_classes = [permissions.AllowAny]


@method_decorator(csrf_exempt, name='dispatch')
class Transaccion(View):
    def post(self, request):

        data = json.loads(request.body.decode("utf-8"))
        no_tarjeta = data.get('no_tarjeta')
        nombre_tarjeta = data.get('nombre_tarjeta')
        cvv = data.get('cvv')
        fecha_vencimiento = data.get('fecha_vencimiento')
        id_producto = data.get('id_producto')
        nombre_producto = data.get('nombre_producto')
        usuario_comprador = data.get('usuario_comprador')
        fecha_peticion = data.get('fecha_peticion')
        
        estado_actual = Estado_Servidor.objects.order_by(
            '-fecha').first().estado
        pago = Pago(no_tarjeta=no_tarjeta, nombre_tarjeta=nombre_tarjeta,
                    cvv=cvv, fecha_vencimiento=fecha_vencimiento)
        pago.save()
        if estado_actual == 1:
            tr=Transaccion_Autorizado(id_producto=id_producto, nombre_producto=nombre_producto,
                                   usuario_comprador=usuario_comprador, fecha_peticion=fecha_peticion, fecha_autorizado=date.today(), pago=pago, autorizado=True)
            tr.save()
        elif estado_actual == 2:
            tr=Transaccion_Autorizado(id_producto=id_producto, nombre_producto=nombre_producto,
                                   usuario_comprador=usuario_comprador, fecha_peticion=fecha_peticion, fecha_authorizado=date.today(), pago=pago, autorizado=False)
            tr.save()
        else:
            tp=Transaccion_Pendiente(id_producto=id_producto, nombre_producto=nombre_producto,
                                   usuario_comprador=usuario_comprador, fecha_peticion=fecha_peticion, pago=pago)
            tp.save()
        # product_data = {
        #     'product_name': nombre_producto,
        # }
        print("nombre_producto:")
        print(nombre_producto)
        data = {
            "message": f"New item added to Cart with id: {nombre_producto}",
            "estado": estado_actual
        }
        return JsonResponse(data, status=201)
