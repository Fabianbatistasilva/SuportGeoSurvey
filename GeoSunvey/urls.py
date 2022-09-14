from django.urls import include, path
from rest_framework import routers
from . import views
from GeoSunvey.views import *

router = routers.DefaultRouter()

router.register(r'Atendimento', OcorrenciaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'Equipamentos', ProdutoViewSet)

urlpatterns = [
    path("api_Ocorrencia/", include(router.urls)),
    path('', views.home, name='home'),
    path('search_resultado/', views.search_resultado, name='search_resultado'),
    path('date_resultado/', views.date_resultado, name='date_resultado'),
    path('logout/', views.logout_user, name='logout'),
    path('atendimento/',views.form_atendimento,name='atender'),
    path('createprodutos/',views.createproduto,name='createprodutos'),
    path('createclientes/',views.cliente,name='createclientes'),
    path('produtos/',views.listproduto,name='produtos'),
    path('clientes/',views.listcliente,name='clientes'),
    path('deletecliente/<int:id>/',views.deletecliente,name='deletecliente'),
    path('editcliente/<int:id>/',views.editcliente,name='editcliente'),
    path('ocorrenciauser/<int:id>/',views.ocorrenciauser,name='ocorrenciauser'),
    path('deletecorrencia/<int:id>/',views.deletecorrencia,name='deletecorrencia'),
    path('deleteproduto/<int:id>/',views.deleteproduto,name='deleteproduto'),
    path('editproduto/<int:id>/',views.editproduto,name='editproduto'),
    path('createtipoprodutos/',views.createtipoprodutos,name='createtipoprodutos'),
    path('metas/',views.listmetas,name='listmeta'),
    path('vendas/',views.listvenda,name='listvenda'),
    path('ocorrencia/',views.listocorrencia,name='listocorrencia'),
    path('addmetas/',views.addmetas,name='addmetas'),
    path('addvendas/',views.addvenda,name='addvenda'),
    path('updatemeta/<int:id>/',views.editmeta,name='editmeta'),
    path('updatevenda/<int:id>/',views.editvendas,name='editvenda'),
    path('deletemeta/<int:id>/',views.deletemeta,name='deletemeta'),
    path('deletevenda/<int:id>/',views.deletevenda,name='deletevenda'),
    path('vendauser/<int:id>/',views.vendauser,name='vendauser'),
    path('metauser/<int:id>/',views.metauser,name='metauser'),
    path('acrecentoAtender/<int:id>/',views.acrecentoAtender,name='acrecentoAtender'),
    path('pesquisacliente/',views.pesquisacliente,name='pesquisacliente'),
    path('pesquisaatendimento/',views.pesquisaatendimento,name='pesquisaatendimento'),
    path('pesquisavenda/',views.pesquisavenda,name='pesquisavenda'),
    path('pesquisaproduto/',views.pesquisaproduto,name='pesquisaproduto'),
    path('finalizarOcorrencia/<int:id>/',views.finalizarocorrencia,name='finalizarocorrencia'),
    path('abrirOcorrencia/<int:id>/',views.finalizarocorrencia,name='abrirocorrencia'),
    path('licenças/',views.licenças,name='licenças'),


    #licença de Série
    path('LicençadeSerie/',views.licençasSerie,name='LicençadeSerie'),
    path('LicençadeSerieEspecifica/<int:id>/',views.licençasSerieEspecifica,name='LicençadeSerieEspecifica'),
    path('LicençadeSerieEditar/<int:id>/',views.EditarLicencaSerie,name='LicençadeSerieEditar'),
    path('deletarlicencaSerie/<int:id>/',views.deletarlicencaserie,name='deletarlicencaserie'),
    path('createlicencaSerie/',views.createlicençasSerie,name='createlicencaserie'),


    #licença de XPAD
    path('licençasXPAD/',views.licencaxpad,name='licençasXPAD'),
    path('licençasXPADEspecifica/<int:id>/',views.licencaxpadEspecifica,name='licençasXPADEspecifica'),
    path('deletarlicencaxpad/<int:id>/',views.deletarlicencaxpad,name='deletarlicencaxpad'),
    path('LicençaXPADEditar/<int:id>/',views.EditarLicencaXpad,name='EditarLicencaXpad'),
    path('createXpad/',views.createlicençasXPAD,name='createxpad'),


    #licença de SURVX
    path('licençasSURVX/',views.licencasurvx,name='licençasSurvX'),
    path('LicençaSurvXEspecifica/<int:id>/',views.licençasSurvXEspecifica,name='LicençaSurvXEspecifica'),
    path('CreatelicençasSURVX/',views.createlicençasSurvX,name='CreatelicencasSURVX'),
    path('LicençaSurvXEditar/<int:id>/',views.EditarLicencaSurvx,name='EditarLicencaSurvx'),
    path('deletarlicencaSurvx/<int:id>/',views.deletarlicencaSurvX,name='deletarlicencaSurvX'),


    #licença de APLITOP
    path('LicençaAplitop/',views.licençasAplitop,name='LicençaAplitop'),
    path('LicençadeAplitopEspecifica/<int:id>/',views.LicençadeAplitopEspecifica,name='LicençadeAplitopEspecifica'),
    path('createAplitop/',views.createlicençasAplitop,name='createlicençasAplitop'),
    path('LicençaAplitopEditar/<int:id>/',views.EditarLicencaAplitop,name='EditarLicencaAplitop'),
    path('deletarlicencaaplitop/<int:id>/',views.deletarlicencaaplitop,name='deletarlicencaaplitop'),


    #licença de SurPad
    path('LicencaSurPad/',views.licençassurpad,name='LicencaSurPad'),
    path('createSurpad/',views.createlicençasSurpad,name='createlicençasSurpad'),
    path('LicençadeSurpadEspecifica/<int:id>/',views.licençasSurpadEspecifica,name='LicençadeSurpadEspecifica'),
    path('LicençaSurpadEditar/<int:id>/',views.EditarLicencaSurpad,name='EditarLicencaSurpad'),
    path('deletarlicencasurpad/<int:id>/',views.deletarLicencasurpad,name='deletarLicencasurpad'),


    #licença de GeoMax
    path('LicençaGeoMax/',views.licençasgeomax,name='LicençaGeoMax'),
    path('LicençaGeoMaxEspecifica/<int:id>/',views.licençasGeoEspecifica,name='LicençaGeoMaxEspecifica'),
    path('LicençaGeoMaxEditar/<int:id>/',views.EditarLicencaGeomax,name='LicençaGeoMaxEditar'),
    path('deletarlicencageomax/<int:id>/',views.deletarLicencageomax,name='deletarLicencageomax'),
    path('createlicencageomax/',views.createlicençasgeomax,name='createlicencageomax'),

    
    #licença kits de locação
    path('kitlocacao/',views.kitlocacao,name='kitlocacao'),
    path('kitlocacaoEspecifica/<int:id>/',views.kitlocacaoEspecifica,name='kitlocacaoEspecifica'),
    path('createkitlocacao/',views.createkitlocacao,name='createkitlocacao'),
    path('LicençakitEditar/<int:id>/',views.EditarLicencakit,name='LicençakitEditar'),
    path('deletarkit/<int:id>/',views.deletarkit,name='deletarkit'),
]