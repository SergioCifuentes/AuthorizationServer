from django.shortcuts import render, redirect
from django.contrib import auth, messages 
# Create your views here.


def signin(request):

    context = {}
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:

            auth.login(request, user)
            return render(request, 'lista_productos.html')
        else:

            messages.error(request, 'invalid username or password')
            return redirect("/authorization/signin")

    else:
        
        return render(request, "login.html", context)
