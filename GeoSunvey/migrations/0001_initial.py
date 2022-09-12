# Generated by Django 4.0.6 on 2022-07-16 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, choices=[('F', 'PF'), ('J', 'PJ'), ('G', 'Governo')], max_length=8, null=True)),
                ('nome', models.CharField(max_length=200, verbose_name='Cliente')),
                ('telefone', models.CharField(blank=True, max_length=200, verbose_name='Telefone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Funcionarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Suporte', 'Suporte Técnico'), ('Venda', 'Vendas'), ('Direto', 'Diretoria'), ('Administrativo', 'administrativo')], max_length=70)),
                ('nome', models.CharField(max_length=200, verbose_name='nome')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('password', models.CharField(max_length=255)),
                ('telefone', models.CharField(blank=True, max_length=200, null=True, verbose_name='Telefone')),
            ],
        ),
        migrations.CreateModel(
            name='metaEquipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Equipe', models.CharField(blank=True, max_length=255, null=True)),
                ('objetivo', models.CharField(max_length=255)),
                ('data', models.DateField(blank=True, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Meta',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('modelo', models.CharField(max_length=255, verbose_name='Modelo')),
                ('marca', models.CharField(blank=True, max_length=255, verbose_name='Marca')),
                ('quantidade', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='tiposProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Vendas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(blank=True, max_length=255, null=True)),
                ('cidade', models.CharField(blank=True, max_length=255, null=True)),
                ('modelo', models.CharField(blank=True, max_length=255, null=True)),
                ('numerodeSerie', models.CharField(blank=True, max_length=255, null=True)),
                ('dataEntrega', models.DateField(blank=True, null=True)),
                ('Observaçoes', models.TextField(blank=True, null=True)),
                ('preco', models.DecimalField(decimal_places=0, max_digits=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Produto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.produto')),
                ('cliente', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.cliente')),
            ],
            options={
                'verbose_name_plural': 'Vendas',
            },
        ),
        migrations.AddField(
            model_name='produto',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.tiposproduto'),
        ),
        migrations.CreateModel(
            name='Ocorrencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, max_length=255, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Finalizado', 'Finalizado'), ('Aberto', 'Aberto'), ('Atendendo', 'Atendendo')], default=False, max_length=100, verbose_name='Status')),
                ('file', models.FileField(blank=True, null=True, upload_to='ocorrencia')),
                ('compra', models.DateField(blank=True, null=True, verbose_name='Compra')),
                ('garantia', models.DateField(blank=True, null=True, verbose_name='Garantia')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.cliente')),
                ('criador', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.funcionarios')),
                ('equipamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.produto')),
            ],
            options={
                'verbose_name_plural': 'Ocorrência',
            },
        ),
        migrations.CreateModel(
            name='Atualizar_Ocorrência',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, max_length=255, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(verbose_name='Status')),
                ('file', models.FileField(blank=True, null=True, upload_to='atendimentosfilesatualizado/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('atualizar_atendimento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.ocorrencia')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.cliente')),
                ('equipamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='GeoSunvey.produto')),
            ],
            options={
                'verbose_name_plural': 'atualização Ocorrência',
            },
        ),
    ]