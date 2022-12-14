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
    path('licen??as/',views.licen??as,name='licen??as'),


    #licen??a de S??rie
    path('Licen??adeSerie/',views.licen??asSerie,name='Licen??adeSerie'),
    path('Licen??adeSerieEspecifica/<int:id>/',views.licen??asSerieEspecifica,name='Licen??adeSerieEspecifica'),
    path('Licen??adeSerieEditar/<int:id>/',views.EditarLicencaSerie,name='Licen??adeSerieEditar'),
    path('deletarlicencaSerie/<int:id>/',views.deletarlicencaserie,name='deletarlicencaserie'),
    path('createlicencaSerie/',views.createlicen??asSerie,name='createlicencaserie'),


    #licen??a de XPAD
    path('licen??asXPAD/',views.licencaxpad,name='licen??asXPAD'),
    path('licen??asXPADEspecifica/<int:id>/',views.licencaxpadEspecifica,name='licen??asXPADEspecifica'),
    path('deletarlicencaxpad/<int:id>/',views.deletarlicencaxpad,name='deletarlicencaxpad'),
    path('Licen??aXPADEditar/<int:id>/',views.EditarLicencaXpad,name='EditarLicencaXpad'),
    path('createXpad/',views.createlicen??asXPAD,name='createxpad'),


    #licen??a de SURVX
    path('licen??asSURVX/',views.licencasurvx,name='licen??asSurvX'),
    path('Licen??aSurvXEspecifica/<int:id>/',views.licen??asSurvXEspecifica,name='Licen??aSurvXEspecifica'),
    path('Createlicen??asSURVX/',views.createlicen??asSurvX,name='CreatelicencasSURVX'),
    path('Licen??aSurvXEditar/<int:id>/',views.EditarLicencaSurvx,name='EditarLicencaSurvx'),
    path('deletarlicencaSurvx/<int:id>/',views.deletarlicencaSurvX,name='deletarlicencaSurvX'),


    #licen??a de APLITOP
    path('Licen??aAplitop/',views.licen??asAplitop,name='Licen??aAplitop'),
    path('Licen??adeAplitopEspecifica/<int:id>/',views.Licen??adeAplitopEspecifica,name='Licen??adeAplitopEspecifica'),
    path('createAplitop/',views.createlicen??asAplitop,name='createlicen??asAplitop'),
    path('Licen??aAplitopEditar/<int:id>/',views.EditarLicencaAplitop,name='EditarLicencaAplitop'),
    path('deletarlicencaaplitop/<int:id>/',views.deletarlicencaaplitop,name='deletarlicencaaplitop'),


    #licen??a de SurPad
    path('LicencaSurPad/',views.licen??assurpad,name='LicencaSurPad'),
    path('createSurpad/',views.createlicen??asSurpad,name='createlicen??asSurpad'),
    path('Licen??adeSurpadEspecifica/<int:id>/',views.licen??asSurpadEspecifica,name='Licen??adeSurpadEspecifica'),
    path('Licen??aSurpadEditar/<int:id>/',views.EditarLicencaSurpad,name='EditarLicencaSurpad'),
    path('deletarlicencasurpad/<int:id>/',views.deletarLicencasurpad,name='deletarLicencasurpad'),


    #licen??a de GeoMax
    path('Licen??aGeoMax/',views.licen??asgeomax,name='Licen??aGeoMax'),
    path('Licen??aGeoMaxEspecifica/<int:id>/',views.licen??asGeoEspecifica,name='Licen??aGeoMaxEspecifica'),
    path('Licen??aGeoMaxEditar/<int:id>/',views.EditarLicencaGeomax,name='Licen??aGeoMaxEditar'),
    path('deletarlicencageomax/<int:id>/',views.deletarLicencageomax,name='deletarLicencageomax'),
    path('createlicencageomax/',views.createlicen??asgeomax,name='createlicencageomax'),

    
    #licen??a kits de loca????o
    path('kitlocacao/',views.kitlocacao,name='kitlocacao'),
    path('kitlocacaoEspecifica/<int:id>/',views.kitlocacaoEspecifica,name='kitlocacaoEspecifica'),
    path('createkitlocacao/',views.createkitlocacao,name='createkitlocacao'),
    path('Licen??akitEditar/<int:id>/',views.EditarLicencakit,name='Licen??akitEditar'),
    path('deletarkit/<int:id>/',views.deletarkit,name='deletarkit'),
]