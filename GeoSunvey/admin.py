from django.contrib import admin

from GeoSunvey.models import KitLocacao,LicençaAplitop, LicençaSURVX,Ocorrencia,Cliente,Produto, Vendas, LicençaGeoMax, LicençaSurPad, LicençaXPAD, LicençadeSerie, metaEquipe,tiposProduto,Atualizar_Ocorrência,Funcionarios


@admin.register(Funcionarios)
@admin.register(tiposProduto)
@admin.register(Atualizar_Ocorrência)
@admin.register(Vendas)
@admin.register(metaEquipe)
@admin.register(Ocorrencia)
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    '''Admin View for '''
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    '''Admin View for '''
    search_fields = ('name','marca','modelo',)
    list_filter = ('marca',)

@admin.register(LicençaGeoMax)
class Admin(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('cliente','cidade','Serial_Number')
    list_filter = ('cidade',)
    search_fields = ('cliente','cidade',)
@admin.register(LicençadeSerie)
class Admin(admin.ModelAdmin):
    '''Admin View for '''
    search_fields = ('cliente','cidade','Produto',)
    list_display = ('cliente','Produto','cidade')
    list_filter = ('Produto','cidade')
@admin.register(LicençaSurPad)
class LicençaSurPadAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('cliente','licença','Serial_Number',)
    search_fields = ('cliente',)
    list_filter = ('data_de_entrega',)


@admin.register(LicençaXPAD)
class LicençaXPADAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('cliente','licença','Transfer_ID',)
    search_fields = ('cliente','data_de_entrega')
    list_filter = ('data_de_entrega',)
@admin.register(LicençaSURVX)
class LicençaSURVXAdmin(admin.ModelAdmin):
    '''Admin View for LicençaSURVX'''

    list_display = ('cliente','Serial_Number',)

@admin.register(LicençaAplitop)
class LicençaAplitopAdmin(admin.ModelAdmin):
    '''Admin View for LicençaAplitop'''

    list_display = ('cliente','licença','status',)

@admin.register(KitLocacao)
class KitLocacaoAdmin(admin.ModelAdmin):
    '''Admin View for KitLocacao'''

    list_display = ('modelo','Serial_Number','Aplicativo',)