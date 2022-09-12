from django.contrib import admin

from GeoSunvey.models import KitLocacao,LicençaAplitop, LicençaSURVX,Ocorrencia,Cliente,Produto, Vendas, LicençaGeoMax, LicençaSurPad, LicençaXPAD, LicençadeSerie, metaEquipe,tiposProduto,Atualizar_Ocorrência,Funcionarios


@admin.register(Funcionarios)
@admin.register(tiposProduto)
@admin.register(Atualizar_Ocorrência)
@admin.register(Vendas)
@admin.register(metaEquipe)
@admin.register(Ocorrencia)
@admin.register(LicençadeSerie)
@admin.register(LicençaGeoMax)
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    '''Admin View for '''
    search_fields = ('nome__icontains',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    '''Admin View for '''
    search_fields = ('name','marca','modelo',)


@admin.register(LicençaSurPad)
class LicençaSurPadAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('cliente','licença','Serial_Number',)
    search_fields = ('cliente',)


@admin.register(LicençaXPAD)
class LicençaXPADAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('cliente','licença','Serial_Number',)
    search_fields = ('cliente',)
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