from django.shortcuts import render, redirect
from django.contrib import auth, messages 
from .models import *
from datetime import datetime
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
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
        estado=request.POST['estados']
        nuevo_estado =Estado_Servidor(estado=estado,fecha=datetime.now())
        nuevo_estado.save()
        return redirect('/authorization/home')
    else:
        context = {'estado':Estado_Servidor.objects.order_by('-fecha').first()
        }
        return render(request,"home.html", context)



class EstadoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Estado_Servidor.objects.order_by('-fecha')
    serializer_class = EstadoSerializer
    permission_classes = [permissions.IsAuthenticated]

