from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator


class tiposProduto(models.Model):
    tipo = models.CharField(max_length=255)
    def __str__(self):
        return self.tipo 
    
class Funcionarios(models.Model):
    TIPOS_CHOICES = (
        ("Suporte", "Suporte Técnico"),
        ("Venda", "Vendas"),
        ("Direto", "Diretoria"),
        ("Administrativo", "administrativo"),
    )
    tipo = models.CharField(max_length=70, choices=TIPOS_CHOICES, blank=False, null=False)
    nome = models.CharField(verbose_name='nome',max_length=200)
    email = models.EmailField(verbose_name='Email',blank=True,null=True)
    password=models.CharField(max_length=255)
    telefone = models.CharField(verbose_name='Telefone',max_length=200,blank=True,null=True)
    def __str__(self):
        return self.nome
    
    
class Cliente(models.Model):
    TIPOS_CHOICES = (
        ("F", "PF"),
        ("J", "PJ"),
        ("G", "Governo")
    )
    tipo = models.CharField(max_length=8, choices=TIPOS_CHOICES, blank=True, null=True)
    nome = models.CharField(verbose_name='Cliente',max_length=200)
    telefone = models.CharField(verbose_name='Telefone',max_length=200,blank=True)
    email=models.EmailField(verbose_name='Email',blank=True)
    def __str__(self):
        return self.nome
    class Meta:
       ordering = ['nome']
    
class Produto(models.Model):
    name = models.CharField(max_length=255,verbose_name='Nome')
    modelo = models.CharField(max_length=255,verbose_name='Modelo')
    marca = models.CharField(max_length=255,verbose_name='Marca',blank=True)
    tipo = models.ForeignKey(tiposProduto,on_delete=models.DO_NOTHING,blank=True,null=True)
    quantidade=models.DecimalField(max_digits=25,decimal_places=2,blank=True,null=True)
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['name']

    def __str__(self):
        return self.name
       
class Ocorrencia(models.Model):
    TIPOS_CHOICES = (
        ("Finalizado", "Finalizado"),
        ("Aberto", "Aberto"),
        ("Atendendo", "Atendendo")
    )
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING) 
    tipo = models.CharField(max_length=255,blank=True,null=True)    
    descricao = models.TextField(null=True, blank=True)
    equipamento = models.ForeignKey(Produto,on_delete=models.DO_NOTHING,null=True)
    status = models.CharField(verbose_name='Status',default=False,max_length=100,choices=TIPOS_CHOICES)
    file = models.FileField(upload_to ='ocorrencia',blank=True,null=True)
    compra = models.DateField(verbose_name='Compra',blank=True,null=True)
    garantia = models.DateField(verbose_name='Garantia',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    criador = models.ForeignKey(Funcionarios,on_delete=models.DO_NOTHING)
    def __str__(self):
        return str(self.tipo)
    class Meta:
        verbose_name_plural = "Ocorrência"


class Atualizar_Ocorrência(models.Model):
    atualizar_atendimento = models.ForeignKey(Ocorrencia,on_delete=models.DO_NOTHING)
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING) 
    tipo = models.CharField(max_length=255,blank=True,null=True)   
    descricao = models.TextField(null=True, blank=True)
    equipamento = models.ForeignKey(Produto,on_delete=models.DO_NOTHING,null=True)
    status = models.BooleanField(verbose_name='Status')
    file = models.FileField(upload_to ='atendimentosfilesatualizado/',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.tipo
    class Meta:
        verbose_name_plural = "atualização Ocorrência"
 
 
class metaEquipe(models.Model):
    Equipe = models.CharField(max_length=255,blank=True,null=True)
    objetivo = models.CharField(max_length=255)
    data = models.DateField(blank=True,null=True)
    descricao = models.TextField(blank=True,null=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.objetivo
    class Meta:
        verbose_name_plural = "Meta"
 

class Vendas(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.DO_NOTHING,blank=True)
    empresa=models.CharField(max_length=255,blank=True,null=True)
    cidade=models.CharField(max_length=255,blank=True,null=True)
    Produto=models.ForeignKey(Produto,on_delete=models.DO_NOTHING)
    modelo=models.CharField(max_length=255,blank=True,null=True)
    numerodeSerie=models.CharField(max_length=255,blank=True,null=True)
    dataEntrega=models.DateField(blank=True,null=True)
    Observaçoes=models.TextField(blank=True,null=True)
    preco=models.DecimalField(decimal_places=00,max_digits=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.cliente)
    class Meta:
        verbose_name_plural = "Vendas"

class LicençadeSerie(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.DO_NOTHING,blank=True)
    empresa=models.CharField(max_length=255,blank=True,null=True)
    cidade=models.CharField(max_length=255,blank=True,null=True)
    Produto=models.ForeignKey(Produto,on_delete=models.DO_NOTHING,blank=True,null=True)
    numerodeSerie=models.CharField(max_length=255,blank=True,null=True)
    Observaçoes=models.TextField(blank=True,null=True)
    def __str__(self):
        return str(self.cliente)+' Nºde série: '+str(self.numerodeSerie)
    class Meta:
        verbose_name_plural = "Licenças de Série"

class LicençaGeoMax(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.DO_NOTHING,blank=True)
    cidade=models.CharField(max_length=255,blank=True,null=True)
    descriçao = models.TextField(blank=True,null=True)
    Equipamento_Number=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number=models.CharField(max_length=255,blank=True,null=True)
    situacao=models.TextField(blank=True,null=True)
    def __str__(self):
        return str(self.cliente)+' Nºde série: '+str(self.Serial_Number)
    class Meta:
        verbose_name_plural = "Licenças do GGO"

    
class LicençaSurPad(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.DO_NOTHING,blank=True)
    licença=models.CharField(max_length=255,blank=True,null=True)
    Transfer_ID=models.CharField(max_length=255,blank=True,null=True)
    modelo=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number=models.CharField(max_length=255,blank=True,null=True)
    situacao=models.TextField(blank=True,null=True)
    data_de_entrega=models.DateField(blank=True,null=True)
    def __str__(self):
        return str(self.cliente)+' Nºde série: '+str(self.Serial_Number)
    class Meta:
        verbose_name_plural = "Licenças do SurPad"

class LicençaXPAD(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.DO_NOTHING,blank=True)
    licença=models.CharField(max_length=255,blank=True,null=True)
    Transfer_ID=models.CharField(max_length=255,blank=True,null=True)
    modelo=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number=models.CharField(max_length=255,blank=True,null=True)
    Equipamento_Number=models.CharField(max_length=255,blank=True,null=True)
    situacao=models.TextField(blank=True,null=True)
    descriçao = models.TextField(blank=True,null=True)
    data_de_entrega=models.DateField(blank=True,null=True)
    def __str__(self):
        return str(self.cliente)+' Nºde série: '+str(self.Serial_Number)
    class Meta:
        verbose_name_plural = "Licenças do X-PAD"

class LicençaSURVX(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.DO_NOTHING,blank=True)
    licença=models.CharField(max_length=255,blank=True,null=True)
    Transfer_ID=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number=models.CharField(max_length=255,blank=True,null=True)
    Equipamento_Number=models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return str(self.cliente)+' Nºde série: '+str(self.Serial_Number)
    class Meta:
        verbose_name_plural = "Licenças do SurvX Sanding"
    

class LicençaAplitop(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.DO_NOTHING,blank=True)
    licença=models.CharField(max_length=255,blank=True,null=True)
    data_de_ativacao=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number=models.CharField(max_length=255,blank=True,null=True)
    status=models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return str(self.cliente)+' Nºde série: '+str(self.Serial_Number)
    class Meta:
        verbose_name_plural = "Licenças do Aplitop"


class KitLocacao(models.Model):
    modelo=models.CharField(max_length=255,blank=True,null=True)
    modelo_coletora=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number_base=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number_rover=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number_coletora=models.CharField(max_length=255,blank=True,null=True)
    Serial_Number=models.CharField(max_length=255,blank=True,null=True)
    Aplicativo=models.CharField(max_length=255,blank=True,null=True)
    Número_do_Kit=models.CharField(max_length=255,blank=True,null=True)
    Equipment_ID=models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return str(self.modelo)+' Nºde série: '+str(self.Serial_Number)
    class Meta:
        verbose_name_plural = "Kit de Locacao"
