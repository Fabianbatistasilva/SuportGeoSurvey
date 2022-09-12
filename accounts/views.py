from django.shortcuts import redirect, render
from GeoSunvey.models import Ocorrencia,Cliente,Produto, tiposProduto,Funcionarios
from GeoSunvey.serializers import OcorrenciaSerializer,ClienteSerializer,ProdutoSerializer
from django.contrib.auth import authenticate, login,logout
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models.query import Q

def user_login(request):
    if len(request.session.values())>0:
        return redirect('home')
    if request.method == 'POST':
        Email = request.POST.get('Email')
        password = request.POST.get('password')
        user =Funcionarios.objects.filter(email=Email, password=password)
        if len(user)<=0:
            usuario = authenticate(request, username=Email, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
            else:  
                messages.add_message(request, messages.INFO, 'Username ou password incorretas.')
                return render(request, 'usuario/login.html', {})
        else:              
            if user:
                request.user=user[0]
                print(request.user)
                request.session['funcionarios']=user[0].id
                print(request.session['funcionarios'])
                return redirect('home')    
    else:
        return render(request, 'usuario/login.html', {})
        
