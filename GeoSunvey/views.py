from math import prod
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import mixins, permissions, viewsets
from GeoSunvey.models import Funcionarios, KitLocacao, Ocorrencia,Cliente, Vendas, Atualizar_Ocorrência, LicençaAplitop, LicençaGeoMax, LicençaSURVX, LicençaSurPad, LicençaXPAD, LicençadeSerie, metaEquipe,Produto, tiposProduto
from GeoSunvey.serializers import OcorrenciaSerializer,ClienteSerializer,ProdutoSerializer
import requests
from django.contrib.auth import authenticate, login,logout
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models.query import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.datastructures import MultiValueDictKeyError
class OcorrenciaViewSet(viewsets.ModelViewSet):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


def date_resultado(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    pesquisa=request.GET.get("search")
    if len(pesquisa.strip())<=0 or pesquisa =='':
        return render(request,'date_resultado.html',)
    pesquisaocorrencia = Ocorrencia.objects.filter(Q(compra__icontains=pesquisa)|Q(garantia__icontains=pesquisa)|Q(created__icontains=pesquisa)|Q(updated__icontains=pesquisa))
    context={'pesquisaocorrencia':pesquisaocorrencia,}
    return render(request,'date_resultado.html',context)       


def search_resultado(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    pesquisa=request.GET.get("search")
    cliente=Cliente.objects.filter(nome__icontains=pesquisa)
    tipoProduto=tiposProduto.objects.filter(tipo__icontains=pesquisa)
    if len(cliente)==0 :
        pesquisaocorrencia = Ocorrencia.objects.filter(Q(descricao__icontains=pesquisa))
    elif cliente:
        pesquisaocorrencia = Ocorrencia.objects.filter(Q(descricao__icontains=pesquisa)| Q(cliente_id=cliente[0].id))
    if len(pesquisa.strip())<=0 or pesquisa =='':
        messages.add_message(request, messages.INFO, 'Pesquisa é nula.')
        return render(request,'pesquisabase.html',)
    else:
        if tipoProduto:
            pesquisaproduto=Produto.objects.filter(Q(name__icontains=pesquisa)|Q(modelo__icontains=pesquisa)|Q(marca__icontains=pesquisa)|Q(tipo_id=tipoProduto[0].id))
        else:
            pesquisaproduto=Produto.objects.filter(Q(name__icontains=pesquisa)|Q(modelo__icontains=pesquisa)|Q(marca__icontains=pesquisa))
        pesquisacliente=Cliente.objects.filter(Q(nome__icontains=pesquisa)|Q(tipo__icontains=pesquisa)|Q(telefone__icontains=pesquisa)|Q(email__icontains=pesquisa))
        pesquisameta=metaEquipe.objects.filter(Q(Equipe__icontains=pesquisa)|Q(descricao__icontains=pesquisa)|Q(objetivo__icontains=pesquisa))
        context={'pesquisacliente':pesquisacliente,'pesquisaocorrencia':pesquisaocorrencia,'pesquisaproduto':pesquisaproduto,'pesquisameta':pesquisameta,}
        return render(request,'pesquisabase.html',context)


def home(request):
    if len(request.session.values())<=0 :
        return redirect('user_login')
    else:
        if request.user.id:
            user_admin =User.objects.get(id=request.user.id)
            user=None
        else:
            user =Funcionarios.objects.get(id=request.session['funcionarios'])
            user_admin=None
        ocorrencias=Ocorrencia.objects.all().order_by('-created',)
        ocorrencias_aberta=Ocorrencia.objects.filter(status='Aberto')
        p = Paginator(ocorrencias, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # Se o page request (9999) está fora da lista, mostre a última página.
        try:
            ocorrencias = p.page(page)
        except (EmptyPage, InvalidPage):
            ocorrencias = p.page(p.num_pages)
        context={'ocorrencias':ocorrencias,'user':user,'ocorrencias_aberta':ocorrencias_aberta,'user_admin':user_admin}
        return render(request,'home.html',context)

def listmetas(request):
    if len(request.session.values())<=0 :
        return redirect('user_login')
    tabmeta=metaEquipe.objects.all().order_by('created')
    quanti_meta=tabmeta.count()
    p = Paginator(tabmeta, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        tabmeta = p.page(page)
    except (EmptyPage, InvalidPage):
        tabmeta = p.page(p.num_pages)
    context={'tabmeta':tabmeta,'quanti_meta':quanti_meta,}
    return render(request,'metalist.html',context)


def listvenda(request):
    if len(request.session.values())<=0 :
        return redirect('user_login')
    tabvenda=Vendas.objects.all().order_by('created')
    quanti_venda=tabvenda.count()
    p = Paginator(tabvenda, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        tabvenda = p.page(page)
    except (EmptyPage, InvalidPage):
        tabvenda = p.page(p.num_pages)
    context={'tabvenda':tabvenda,'quanti_venda':quanti_venda,}
    return render(request,'vendalist.html',context)

def addmetas(request):
    if len(request.session.values())<=0 :
        return redirect('user_login')
    if request.method == 'POST':
        equipe = request.POST.get('equipe')
        objetivo = request.POST.get('objetivo')
        data = request.POST.get('data')
        descricao = request.POST.get('descricao')
        status = request.POST.get('status')
        if data== '':
            data=None
        if status=='False':
            status=False
            meta = metaEquipe.objects.create(Equipe=equipe, objetivo=objetivo,data=data, descricao=descricao,status=status)
            meta.save()
            messages.add_message(request, messages.SUCCESS, 'Meta Criada com Sucesso.')
            return redirect('listmeta') 
        else:
            status=True
            meta = metaEquipe.objects.create(Equipe=equipe, objetivo=objetivo,data=data, descricao=descricao,status=status)
            meta.save()
            messages.add_message(request, messages.SUCCESS, 'Meta Criada com Sucesso.')
            return redirect('listmeta') 
    else:
        tabmeta=metaEquipe.objects.all()
        quanti_meta=tabmeta.count()
        context={'tabmeta':tabmeta,'quanti_meta':quanti_meta,}
        return render(request,'addmeta.html',context)


def addvenda(request):
    if len(request.session.values())<=0 :
        return redirect('user_login')
    if request.method == 'POST':
            cliente = request.POST.get('cliente')
            empresa = request.POST.get('empresa')
            cidade = request.POST.get('cidade')
            produto = request.POST.get('produto')
            modelo = request.POST.get('modelo')
            numerodeSerie = request.POST.get('numerodeSerie')
            dataEntrega = request.POST.get('dataEntrega')
            Observaçoes = request.POST.get('Observaçoes')
            preco = request.POST.get('preco')
            if cliente==''  or produto=='':
                messages.add_message(request, messages.INFO, 'Coloque os Valores Obrigatórios(Cliente,Produto)')
                return redirect('addvenda')
            else:
                cliente=Cliente.objects.get(nome=cliente)
                produto=Produto.objects.get(name=produto)
                if preco==None or preco=='':
                    preco=0
                if dataEntrega== '':
                    dataEntrega=None
                venda = Vendas.objects.create(cliente_id=cliente.id, empresa=empresa,cidade=cidade, Produto_id=produto.id,modelo=modelo,numerodeSerie=numerodeSerie, dataEntrega=dataEntrega,Observaçoes=Observaçoes, preco=preco)
                venda.save()
                messages.add_message(request, messages.SUCCESS, 'Venda Criada com Sucesso.')
                return redirect('listvenda') 
    else:
        cidades=requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios').json()
        clientes=Cliente.objects.all()
        produtos=Produto.objects.all()
        context={'cidades':cidades,'clientes':clientes,'produtos':produtos}
        return render(request,'addvenda.html',context)


def form_atendimento(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        clientes = request.POST.get('cliente')
        tecnico = request.POST.get('tecnico')
        produto = request.POST.get('produto')
        compra = request.POST.get('compra')
        garantia = request.POST.get('garantia')
        tipoatendimento = request.POST.get('tipoatendimento')
        descricao = request.POST.get('descricao')
        status = request.POST.get('status')
        try:
            file = request.FILES.get('file')
        except MultiValueDictKeyError:
            file = False
        #verificando no banco
        if compra== '':
            compra=None
        if garantia=='':
            garantia=None
        if clientes=='' or tecnico =='' or produto=='' or tipoatendimento=='':
            messages.add_message(request, messages.INFO, 'Coloque os Valores Obrigatórios(Cliente,Técnico,Status,Produto)')
            return redirect('atender')
        else:
            cliente=Cliente.objects.get(nome=clientes)
            tecnico=Funcionarios.objects.filter(nome__icontains=tecnico)
            tecnico=Funcionarios.objects.get(id=tecnico[0].id)
            produtos=Produto.objects.get(name=produto)
            add_atender=Ocorrencia.objects.create(cliente_id=cliente.id,tipo=tipoatendimento,descricao=descricao,equipamento_id=produtos.id,status=status,file=file,compra=compra,garantia=garantia,criador_id=tecnico.id)
            add_atender.save()
            messages.add_message(request, messages.SUCCESS, 'Criado com Sucesso')
            return redirect('listocorrencia')
    else:
        cliente=Cliente.objects.all()
        tecnicos=Funcionarios.objects.all()
        produtos=Produto.objects.all()
        context={'cliente':cliente,'produtos':produtos,'tecnicos':tecnicos}
        return render(request,'atender.html',context)


def createproduto(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method == 'POST':
        name = request.POST.get('name')
        modelo = request.POST.get('modelo')
        marca = request.POST.get('marca')
        tipo = int(request.POST.get('tipoproduto'))
        quantidade = request.POST.get('quantidade')
        venda = Produto.objects.create(name=name, modelo=modelo,marca=marca, tipo_id=tipo,)
        venda.save()
        messages.add_message(request, messages.SUCCESS, 'Produto Criada com Sucesso.')
        return redirect('createprodutos')
    produtostipos=tiposProduto.objects.all()
    context={'produtostipos':produtostipos,}
    return render(request,'createproduto.html',context)


def cliente(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method =='POST':
        nome=request.POST.get('nome')
        tipo=request.POST.get('tipo')
        email=request.POST.get('email')
        telefone=request.POST.get('telefone')
        verifica_clientes=Cliente.objects.filter(nome=nome)
        if len(verifica_clientes)>=1:
            messages.add_message(request, messages.INFO, 'Já existe Cliente com este nome.')
            return render(request,'createcliente.html',)
        if len(nome.strip())<=0 or nome =='':
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'tipoatendercreate.html',)
        add_cliente=Cliente.objects.create(nome=nome,tipo=tipo,email=email,telefone=telefone)
        add_cliente.save()
        messages.add_message(request, messages.SUCCESS, 'Criado com Sucesso')
        return redirect('clientes')
    context={}
    return render(request,'createcliente.html',context)

    
def logout_user(request):
    try:
        del request.session['funcionarios']
        logout(request)
    except KeyError:
        logout(request)
    return redirect('user_login')



def listproduto(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    tabproduto=Produto.objects.all().order_by()
    quanti_produto=tabproduto.count()
    p = Paginator(tabproduto, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        tabproduto = p.page(page)
    except (EmptyPage, InvalidPage):
        tabproduto = p.page(p.num_pages)
    context={'tabproduto':tabproduto,'quanti_produto':quanti_produto,}
    return render(request,'listproduto.html',context)



def listcliente(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    tabcliente=Cliente.objects.all().order_by()
    quanti_clientes=tabcliente.count()
    p = Paginator(tabcliente, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        tabcliente = p.page(page)
    except (EmptyPage, InvalidPage):
        tabcliente = p.page(p.num_pages)
    clientes=Cliente.objects.all().order_by()
    context={'tabcliente':tabcliente,'quanti_clientes':quanti_clientes,'clientes':clientes}
    return render(request,'listcliente.html',context)



def ocorrenciauser(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    ocorrencia=Ocorrencia.objects.get(id=id)
    ocorrencias_aberta=Ocorrencia.objects.filter(status='Aberto')
    atualizacao=Atualizar_Ocorrência.objects.filter(atualizar_atendimento_id=ocorrencia.id)
    context={'ocorrencia':ocorrencia,'ocorrencias_aberta':ocorrencias_aberta,'atualizacao':atualizacao}
    return render(request,'ocorrenciauser.html',context)



def deletecorrencia(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deleteatendimento=Ocorrencia.objects.get(id=id)
        deleteatendimento.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('listocorrencia')
    ocorrencia=Ocorrencia.objects.get(id=id)
    cliente=Cliente.objects.all()
    tipos=tiposProduto.objects.all()
    produtos=Produto.objects.all()
    context={'ocorrencia':ocorrencia,'cliente':cliente,'tipos':tipos,'produtos':produtos,}
    return render(request,'delete_ocorrencia.html',context)





def deletecliente(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletecliente=Cliente.objects.get(id=id)
        deletecliente.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('clientes')
    cliente=Cliente.objects.get(id=id)
    context={'cliente':cliente,}
    return render(request,'delete_cliente.html',context)



def editcliente(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        cliente = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        if len(cliente.split())==0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createtipoprodutos.html',)
        edit=Cliente.objects.filter(id=id).update(tipo=tipo,nome=cliente,telefone=telefone,email=email)
        messages.add_message(request, messages.SUCCESS, 'Editado com Sucesso')
        return redirect('clientes')
        
    cliente=Cliente.objects.get(id=id)
    context={'cliente':cliente,}
    return render(request,'edit_cliente.html',context)



def deleteproduto(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deleteproduto=Produto.objects.get(id=id)
        deleteproduto.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('produtos')    
    cliente=Produto.objects.get(id=id)
    context={'cliente':cliente,}
    return render(request,'delete_cliente.html',context)



def editproduto(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method == 'POST':
        name = request.POST.get('nome')
        modelo = request.POST.get('modelo')
        marca = request.POST.get('marca')
        tipo = request.POST.get('tipoproduto')
        edit = Produto.objects.filter(id=id).update(name=name, modelo=modelo,marca=marca, tipo_id=tipo,)
        messages.add_message(request, messages.SUCCESS, 'Produto Editado com Sucesso.')
        return redirect('produtos')
    produto=Produto.objects.get(id=id)
    tiposproduto=tiposProduto.objects.all()
    context={'tiposproduto':tiposproduto,'produto':produto}
    return render(request,'editproduto.html',context)


def createtipoprodutos(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        tipoProduto=request.POST.get('tipoproduto')
        if len(tipoProduto.split())==0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createtipoprodutos.html',)
        add_tipoProduto=tiposProduto.objects.create(tipo=tipoProduto)
        add_tipoProduto.save()
        messages.add_message(request, messages.SUCCESS, 'Criado com Sucesso')
        return redirect('createtipoprodutos')
    tiposProdutos=tiposProduto.objects.all()
    context={'tiposProdutos':tiposProdutos,}
    return render(request,'createtipoprodutos.html',context)

def deletemeta(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletemeta=metaEquipe.objects.get(id=id)
        deletemeta.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('listmeta')
    meta=metaEquipe.objects.get(id=id)
    context={'meta':meta,}
    return render(request,'delete_meta.html',context)



def editmeta(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method == 'POST':
        equipe = request.POST.get('equipe')
        objetivo = request.POST.get('objetivo')
        data = request.POST.get('data')
        descricao = request.POST.get('descricao')
        status = request.POST.get('status')
        if data== '':
            data=None
        if status=='False':
            status=False
            meta = metaEquipe.objects.filter(id=id).update(Equipe=equipe, objetivo=objetivo,data=data, descricao=descricao,status=status)
            messages.add_message(request, messages.SUCCESS, 'Meta editada com Sucesso.')
            return redirect('listmeta') 
        else:
            status=True
            meta = metaEquipe.objects.filter(id=id).update(Equipe=equipe, objetivo=objetivo,data=data, descricao=descricao,status=status)
            messages.add_message(request, messages.SUCCESS, 'Meta editada com Sucesso.')
            return redirect('listmeta') 
    meta=metaEquipe.objects.get(id=id)
    context={'meta':meta,}
    return render(request,'edit_meta.html',context)


def deletevenda(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletevenda=Vendas.objects.get(id=id)
        deletevenda.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('listvenda')
    venda=Vendas.objects.get(id=id)
    context={'venda':venda,}
    return render(request,'delete_venda.html',context)



def editvendas(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method == 'POST':
            cliente = request.POST.get('cliente')
            empresa = request.POST.get('empresa')
            cidade = request.POST.get('cidade')
            produto = request.POST.get('produto')
            modelo = request.POST.get('modelo')
            numerodeSerie = request.POST.get('numerodeSerie')
            dataEntrega = request.POST.get('dataEntrega')
            Observaçoes = request.POST.get('Observaçoes')
            preco = request.POST.get('preco')
            if cliente==''  or produto=='':
                messages.add_message(request, messages.INFO, 'Coloque os Valores Obrigatórios(Cliente,Produto)')
                return redirect('addvenda')
            else:
                cliente=Cliente.objects.get(nome=cliente)
                produto=Produto.objects.get(name=produto)
                if preco==None or preco=='':
                    preco=0
                if dataEntrega== '':
                    dataEntrega=None
                edit=Vendas.objects.filter(id=id).update(cliente_id=cliente.id, empresa=empresa,cidade=cidade, Produto_id=produto.id,modelo=modelo,numerodeSerie=numerodeSerie, dataEntrega=dataEntrega,Observaçoes=Observaçoes, preco=preco)
                messages.add_message(request, messages.SUCCESS, 'Venda editada com Sucesso.')
                return redirect('listvenda') 
    venda=Vendas.objects.get(id=id)
    cidades=requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios').json()
    clientes=Cliente.objects.all()
    produtos=Produto.objects.all()
    context={'cidades':cidades,'clientes':clientes,'produtos':produtos,'venda':venda}
    return render(request,'edit_venda.html',context)


def listocorrencia(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    ocorrencias=Ocorrencia.objects.all().order_by('-created',)
    p = Paginator(ocorrencias, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        ocorrencias = p.page(page)
    except (EmptyPage, InvalidPage):
        ocorrencias = p.page(p.num_pages)
    context={'ocorrencias':ocorrencias,}
    return render(request,'listocorrencia.html',context)

def vendauser(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    venda=Vendas.objects.get(id=id)
    context={'venda':venda,}
    return render(request,'vendauser.html',context)

def metauser(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    meta=metaEquipe.objects.get(id=id)
    context={'meta':meta,}
    return render(request,'metauser.html',context)

def acrecentoAtender(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    ocorrencia_atual=Ocorrencia.objects.get(id=id)
    if request.method=='POST':
        descricao = request.POST.get('descricao')
        try:
            file = request.FILES.get('file')
        except MultiValueDictKeyError:
            file = False
        try:
            add_comentario=Atualizar_Ocorrência.objects.create(atualizar_atendimento_id=ocorrencia_atual.id,cliente_id=ocorrencia_atual.cliente_id,tipo=ocorrencia_atual.tipo,descricao=descricao,equipamento_id=ocorrencia_atual.equipamento_id,status=True,file=file)
            add_comentario.save()
            messages.add_message(request, messages.SUCCESS, 'Comentado com Sucesso')
            return redirect('listocorrencia')
        except:
            context={'ocorrencia_atual':ocorrencia_atual,}
            messages.add_message(request, messages.INFO, 'Erro ao criar (Campos Inválidos)')
            return render(request,'acrecentoatender.html',context)  
    context={'ocorrencia_atual':ocorrencia_atual,}
    return render(request,'acrecentoatender.html',context)

def pesquisacliente(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    pesquisa=request.GET.get("searchcliente")
    if len(pesquisa.strip())<=0 or pesquisa =='':
        return render(request,'pesquisabase.html',)
    pesquisacliente = Cliente.objects.filter(Q(nome__icontains=pesquisa)|Q(tipo__icontains=pesquisa)|Q(email__icontains=pesquisa)|Q(telefone__icontains=pesquisa))
    context={'pesquisacliente':pesquisacliente,}
    return render(request,'pesquisabase.html',context)     

  
def pesquisaatendimento(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    pesquisa=request.GET.get("searchatendimento")
    if len(pesquisa.strip())<=0 or pesquisa =='':
        return render(request,'pesquisabase.html',)
    cliente=Cliente.objects.filter(nome__icontains=pesquisa)
    if len(cliente)==0 :
        pesquisaocorrencia = Ocorrencia.objects.filter(Q(descricao__icontains=pesquisa)|Q(tipo__icontains=pesquisa))
    elif cliente:
        pesquisaocorrencia = Ocorrencia.objects.filter(Q(descricao__icontains=pesquisa)| Q(cliente_id=cliente[0].id)|Q(tipo__icontains=pesquisa))
    context={'pesquisaocorrencia':pesquisaocorrencia,}
    return render(request,'pesquisabase.html',context)  

def pesquisavenda(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    pesquisa=request.GET.get("search")
    if len(pesquisa.strip())<=0 or pesquisa =='':
        return render(request,'pesquisabase.html',)
    cliente=Cliente.objects.filter(nome__icontains=pesquisa)
    produto=Produto.objects.filter(name__icontains=pesquisa)
    if len(cliente)==0 :
        if produto:
            pesquisavenda = Vendas.objects.filter(Q(dataEntrega__icontains=pesquisa)|Q(created__icontains=pesquisa)|Q(Produto_id=produto[0].id))
        else:
            pesquisavenda = Vendas.objects.filter(Q(dataEntrega__icontains=pesquisa)|Q(created__icontains=pesquisa))
    elif cliente:
        if produto:
            pesquisavenda = Ocorrencia.objects.filter(Q(dataEntrega__icontains=pesquisa)|Q(created__icontains=pesquisa)| Q(cliente_id=cliente[0].id)|Q(Produto_id=produto[0].id))
        else:
            pesquisavenda = Ocorrencia.objects.filter(Q(descricao__icontains=pesquisa)| Q(cliente_id=cliente[0].id)|Q(tipo__icontains=pesquisa))
    context={'pesquisavenda':pesquisavenda,}
    return render(request,'pesquisabase.html',context)


def pesquisaproduto(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    pesquisa=request.GET.get("search")
    tipoProduto=tiposProduto.objects.filter(tipo__icontains=pesquisa)
    if len(pesquisa.strip())<=0 or pesquisa =='':
        return render(request,'pesquisabase.html',)
    if tipoProduto:
        pesquisaproduto=Produto.objects.filter(Q(name__icontains=pesquisa)|Q(modelo__icontains=pesquisa)|Q(marca__icontains=pesquisa)|Q(tipo_id=tipoProduto[0].id))
    else:
        pesquisaproduto=Produto.objects.filter(Q(name__icontains=pesquisa)|Q(modelo__icontains=pesquisa)|Q(marca__icontains=pesquisa))

    context={'pesquisaproduto':pesquisaproduto,}
    return render(request,'pesquisabase.html',context)   

def finalizarocorrencia(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    ocorrencia=Ocorrencia.objects.filter(id=id).update(status='Finalizado')
    messages.add_message(request, messages.SUCCESS, 'Finalizado com Sucesso')
    return redirect('listocorrencia')

def abrircorrencia(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    ocorrencia=Ocorrencia.objects.filter(id=id).update(status='Aberto')
    messages.add_message(request, messages.SUCCESS, 'Finalizado com Sucesso')
    return redirect('listocorrencia')

def licenças(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    licençaserie=LicençadeSerie.objects.all()
    Licençaaplitop=LicençaAplitop.objects.all()
    Licençageomax=LicençaGeoMax.objects.all()
    licencaxpad=LicençaXPAD.objects.all()
    Licençasurpad=LicençaSurPad.objects.all()
    Licençasurvx=LicençaSURVX.objects.all()
    soma= Licençasurvx.count() + Licençasurpad.count() + licencaxpad.count() + licençaserie.count() + Licençageomax.count() + Licençaaplitop.count()
    context={'soma':soma,'licençaserie':licençaserie,'Licençaaplitop':Licençaaplitop,'Licençageomax':Licençageomax,'licencaxpad':licencaxpad,'Licençasurpad':Licençasurpad,'Licençasurvx':Licençasurvx}
    return render(request,'listlicenca.html',context)



### Licenças de Série ###
def licençasSerie(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    licençaserie=LicençadeSerie.objects.all()
    quanti_licenca=licençaserie.count()
    p = Paginator(licençaserie, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        licençaserie = p.page(page)
    except (EmptyPage, InvalidPage):
        licençaserie = p.page(p.num_pages)
    context={'licençaserie':licençaserie,'quanti_licenca':quanti_licenca}
    return render(request,'licencaserie.html',context)


def licençasSerieEspecifica(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    try:
        licençaserie=LicençadeSerie.objects.get(id=id)
    except:
        return redirect('LicençadeSerie')
    context={'licençaserie':licençaserie,}
    return render(request,'licencaserieEspecifica.html',context)


def createlicençasSerie(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        cliente = request.POST.get('cliente')
        empresa = request.POST.get('empresa')    
        cidade = request.POST.get('cidade')    
        produto = request.POST.get('produto')    
        numerodeserie = request.POST.get('numerodeserie')
        Observacao = request.POST.get('Observacao')
        if len(cliente.split())==0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createlicencasurvx.html',)
        cliente = Cliente.objects.filter(nome = cliente)
        produto = Produto.objects.filter(name = produto)
        if len(produto) == 0 or len(cliente) == 0:
            messages.add_message(request, messages.INFO, 'Valores invalido.')
            return render(request,'createlicencaserie.html',)
        add_licenca = LicençadeSerie.objects.create(cliente_id=cliente[0].id,Produto_id=produto[0].id,numerodeSerie=numerodeserie,cidade=cidade,empresa=empresa,Observaçoes = Observacao)
        add_licenca.save()
        return redirect('LicençadeSerie')
    else:
        clientes=Cliente.objects.all()
        produtos=Produto.objects.all()
        context={'clientes':clientes,'produtos':produtos}
        return render(request,'createlicencaserie.html',context)

def EditarLicencaSerie(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        cliente = request.POST.get('cliente')
        empresa = request.POST.get('empresa')    
        cidade = request.POST.get('cidade')    
        produto = request.POST.get('produto')    
        numerodeserie = request.POST.get('numerodeserie')
        Observacao = request.POST.get('Observacao')  
        if len(cliente.split())==0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createlicencasurvx.html',)
        cliente = Cliente.objects.filter(nome = cliente)
        produto = Produto.objects.filter(name = produto)
        if len(produto) == 0 or len(cliente) == 0:
            messages.add_message(request, messages.INFO, 'Valores invalido.')
            return render(request,'createlicencaserie.html',)
        licenca=LicençadeSerie.objects.get(id=id)
        licenca.update(cliente_id=cliente[0].id,Produto_id=produto[0].id,numerodeSerie=numerodeserie,cidade=cidade,empresa=empresa,Observaçoes = Observacao)
    try:
        licenca=LicençadeSerie.objects.get(id=id)
    except:
        return redirect('LicençadeSerie')
    clientes=Cliente.objects.all()
    produtos=Produto.objects.all()
    context={'licenca':licenca,'clientes':clientes,'produtos':produtos}
    return render(request,'licencaEdita.html',context)

    
def deletarlicencaserie(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletelicenca=LicençadeSerie.objects.get(id=id)
        deletelicenca.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('listvenda')
    licenca=LicençadeSerie.objects.get(id=id)
    context={'licenca':licenca,}
    return render(request,'deletarlicenca.html',context)


#GeoMax

def licençasgeomax(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    licençaserie=LicençaGeoMax.objects.all()
    quanti_licenca=licençaserie.count()
    p = Paginator(licençaserie, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        licençaserie = p.page(page)
    except (EmptyPage, InvalidPage):
        licençaserie = p.page(p.num_pages)
    context={'licençaserie':licençaserie,'quanti_licenca':quanti_licenca}
    return render(request,'licencageomax.html',context)

def licençasGeoEspecifica(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    try:
        licençaserie=LicençaGeoMax.objects.get(id=id)
    except:
        return redirect('LicençaGeoMax')
    context={'licençaserie':licençaserie,}
    return render(request,'licencageomaxEspecifica.html',context)

def createlicençasgeomax(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        cliente = request.POST.get('cliente')
        situacao = request.POST.get('situacao')    
        cidade = request.POST.get('cidade')    
        Serial_Number = request.POST.get('Serial_Number')    
        Equipamento_Number = request.POST.get('Equipamento_Number')
        situacao = request.POST.get('situacao')  
        cliente = Cliente.objects.filter(nome = cliente)
        if len(cliente.split()) == 0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createlicencasurvx.html',)
        if  len(cliente) == 0:
            messages.add_message(request, messages.INFO, 'Valores invalido.')
            return render(request,'createlicencageomax.html',)
        add_licenca = LicençaGeoMax.objects.create(cliente_id=cliente[0].id,situacao=situacao,Serial_Number=Serial_Number,cidade=cidade, Equipamento_Number=Equipamento_Number,)
        add_licenca.save()
        return redirect('LicençaGeoMax')
    else:
        clientes=Cliente.objects.all()
        context={'clientes':clientes,}
        return render(request,'createlicencageomax.html',context)


def EditarLicencaGeomax(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        cliente = request.POST.get('cliente')
        situacao = request.POST.get('situacao')    
        cidade = request.POST.get('cidade')    
        Serial_Number = request.POST.get('Serial_Number')    
        Equipamento_Number = request.POST.get('Equipamento_Number')
        situacao = request.POST.get('situacao') 
        if len(cliente.split())==0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createlicencasurvx.html',)
        cliente = Cliente.objects.filter(nome = cliente)
        if  len(cliente) == 0:
            messages.add_message(request, messages.INFO, 'Valores invalido.')
            return render(request,'createlicencaserie.html',)
        licenca=LicençaGeoMax.objects.get(id=id)
        #licenca.update()
    try:
        licenca=LicençaGeoMax.objects.get(id=id)
    except:
        return redirect('LicençaGeoMax')
    clientes=Cliente.objects.all()
    produtos=Produto.objects.all()
    context={'licenca':licenca,'clientes':clientes,'produtos':produtos}
    return render(request,'licencaEdita.html',context)


def deletarLicencageomax(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletelicenca=LicençaGeoMax.objects.get(id=id)
        deletelicenca.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('listvenda')
    licenca=LicençaGeoMax.objects.get(id=id)
    context={'licenca':licenca,}
    return render(request,'deletarlicenca.html',context)

### SurvX ###

def createlicençasSurvX(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        cliente = request.POST.get('cliente')
        licença = request.POST.get('licença')
        Transfer_ID = request.POST.get('Transfer_ID')
        Serial_Number = request.POST.get('Serial_Number')
        Equipamento_Number = request.POST.get('Equipamento_Number')
        if len(cliente.split())==0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createlicencasurvx.html',)
        cliente = Cliente.objects.filter(nome = cliente)
        if  len(cliente) == 0:
            messages.add_message(request, messages.INFO, 'Valores invalido.')
            return render(request,'createlicencasurvx.html',)
        licenca = LicençaSURVX.objects.create(cliente_id=cliente[0].id,licença=licença,Transfer_ID=Transfer_ID,Serial_Number=Serial_Number,Equipamento_Number=Equipamento_Number)
        licenca.save()
        messages.add_message(request, messages.SUCCESS, 'Criado com Sucesso')
        return redirect('licençasSURVX')
    clientes=Cliente.objects.all()
    context={'clientes':clientes,}
    return render(request,'createlicencasurvx.html',context)

def licençasSurvXEspecifica(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    try:
        licençaserie=LicençaSURVX.objects.get(id=id)
    except:
        return redirect('licençasSURVX')
    context={'licençaserie':licençaserie,}
    return render(request,'licencaSurvXEspecifica.html',context)

def deletarlicencaSurvX(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletelicenca=LicençaSURVX.objects.get(id=id)
        deletelicenca.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('licençasSURVX')
    licenca=LicençaSURVX.objects.get(id=id)
    context={'licenca':licenca,}
    return render(request,'deletarlicenca.html',context)

def EditarLicencaSurvx(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        licenca=LicençaSURVX.objects.get(id=id)
        #licenca.update()
    try:
        licenca=LicençaSURVX.objects.get(id=id)
    except:
        return redirect('licençasSURVX')
    clientes=Cliente.objects.all()
    produtos=Produto.objects.all()
    context={'licenca':licenca,'clientes':clientes,'produtos':produtos}
    return render(request,'licencaEdita.html',context)


## Aplitop ##
def licençasAplitop(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    licençaserie=LicençaAplitop.objects.all()
    quanti_licenca=licençaserie.count()
    p = Paginator(licençaserie, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        licençaserie = p.page(page)
    except (EmptyPage, InvalidPage):
        licençaserie = p.page(p.num_pages)
    context={'licençaserie':licençaserie,'quanti_licenca':quanti_licenca}
    return render(request,'licencaAplitop.html',context)

def createlicençasAplitop(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        cliente=request.POST.get('cliente')
        licença=request.POST.get('licença')
        data_de_ativacao=request.POST.get('data_de_ativacao')
        Serial_Number=request.POST.get('Serial_Number')
        status=request.POST.get('status')
        if len(cliente.split())==0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createlicencaAplitop.html',)
        cliente = Cliente.objects.filter(nome = cliente)
        if  len(cliente) == 0:
            messages.add_message(request, messages.INFO, 'Valores invalido.')
            return render(request,'createlicencaAplitop.html',)
        licenca=LicençaAplitop.objects.create(cliente_id=cliente[0].id,licença=licença,data_de_ativacao=data_de_ativacao,Serial_Number=Serial_Number,status=status)
        licenca.save()
        messages.add_message(request, messages.SUCCESS, 'Criado com Sucesso')
        return redirect('LicençaAplitop')
    clientes=Cliente.objects.all()
    context={'clientes':clientes,}
    return render(request,'createlicencaAplitop.html',context)

def deletarlicencaaplitop(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletelicenca=LicençaAplitop.objects.get(id=id)
        deletelicenca.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('LicençaAplitop')
    licenca=LicençaAplitop.objects.get(id=id)
    context={'licenca':licenca,}
    return render(request,'deletarlicenca.html',context)

def EditarLicencaAplitop(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        licenca=LicençaAplitop.objects.get(id=id)
        #licenca.update()
    try:
        licenca=LicençaAplitop.objects.get(id=id)
    except:
        return redirect('LicençaAplitop')
    clientes=Cliente.objects.all()
    produtos=Produto.objects.all()
    context={'licenca':licenca,'clientes':clientes,'produtos':produtos}
    return render(request,'licencaEdita.html',context)

def LicençadeAplitopEspecifica(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    try:
        licençaserie=LicençaAplitop.objects.get(id=id)
    except:
        return redirect('LicençaAplitop')
    context={'licençaserie':licençaserie,}
    return render(request,'licencaAplitopEspecifica.html',context)
#Licença Surpad#

def deletarLicencasurpad(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletelicenca=LicençaSurPad.objects.get(id=id)
        deletelicenca.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('LicencaSurPad')
    licenca=LicençaSurPad.objects.get(id=id)
    context={'licenca':licenca,}
    return render(request,'deletarlicenca.html',context)


def createlicençasSurpad(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        cliente=request.POST.get('cliente')
        licença=request.POST.get('licença')
        Transfer_ID=request.POST.get('Transfer_ID')
        Serial_Number=request.POST.get('Serial_Number')
        situacao=request.POST.get('situacao')
        modelo=request.POST.get('modelo')
        if len(cliente.split())==0:
            messages.add_message(request, messages.INFO, 'Valor invalido.')
            return render(request,'createlicencasurpad.html',)
        cliente = Cliente.objects.filter(nome = cliente)
        if  len(cliente) == 0:
            messages.add_message(request, messages.INFO, 'Valores invalido.')
            return render(request,'createlicencasurpad.html',)
        licenca=LicençaSURVX.objects.create(cliente_id=cliente[0].id,licença=licença,Transfer_ID=Transfer_ID,Serial_Number=Serial_Number,modelo=modelo,situacao=situacao)
        licenca.save()
        messages.add_message(request, messages.SUCCESS, 'Criado com Sucesso')
        return redirect('LicencaSurPad')
    clientes=Cliente.objects.all()
    context={'clientes':clientes,}
    return render(request,'createlicencasurpad.html',context)

def licençassurpad(request):
    if len(request.session.values())<=0:
        return redirect('user_login')
    licençasurpad=LicençaSurPad.objects.all()
    quanti_licenca=licençasurpad.count()
    p = Paginator(licençasurpad, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        licençasurpad = p.page(page)
    except (EmptyPage, InvalidPage):
        licençasurpad = p.page(p.num_pages)
    context={'licençasurpad':licençasurpad,'quanti_licenca':quanti_licenca}
    return render(request,'licencaSurpad.html',context)


def licençasSurpadEspecifica(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    try:
        licençaserie=LicençaSurPad.objects.get(id=id)
    except:
        return redirect('LicencaSurPad')
    context={'licençaserie':licençaserie,}
    return render(request,'licencaSurpadEspecifica.html',context)



def EditarLicencaSurpad(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        licenca=LicençaSurPad.objects.get(id=id)
        #licenca.update()
    try:
        licenca=LicençaSurPad.objects.get(id=id)
    except:
        return redirect('LicencaSurPad')
    clientes=Cliente.objects.all()
    produtos=Produto.objects.all()
    context={'licenca':licenca,'clientes':clientes,'produtos':produtos,}
    return render(request,'licencaEdita.html',context) 
     
#####################
def deletarlicencaxpad(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletelicenca=LicençaXPAD.objects.get(id=id)
        deletelicenca.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('licençasXPAD')
    licenca=LicençaXPAD.objects.get(id=id)
    context={'licenca':licenca,}
    return render(request,'deletarlicenca.html',context)

def EditarLicencaXpad(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        licenca=LicençaXPAD.objects.get(id=id)
        #licenca.update()
    try:
        licenca=LicençaXPAD.objects.get(id=id)
    except:
        return redirect('licençasXPAD')
    clientes=Cliente.objects.all()
    produtos=Produto.objects.all()
    context={'licenca':licenca,'clientes':clientes,'produtos':produtos,}
    return render(request,'licencaEdita.html',context) 

########################
def deletarkit(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        deletelicenca=KitLocacao.objects.get(id=id)
        deletelicenca.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect('kitlocacao')
    licenca=KitLocacao.objects.get(id=id)
    context={'licenca':licenca,}
    return render(request,'deletarlicenca.html',context)

def EditarLicencakit(request,id):
    if len(request.session.values())<=0:
        return redirect('user_login')
    if request.method=='POST':
        licenca=KitLocacao.objects.get(id=id)
        licenca.update()
    try:
        licenca=KitLocacao.objects.get(id=id)
    except:
        return redirect('kitlocacao')
    clientes=Cliente.objects.all()
    produtos=Produto.objects.all()
    context={'licenca':licenca,'clientes':clientes,'produtos':produtos}
    return render(request,'licencaEdita.html',context) 