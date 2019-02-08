# Generated by Django 2.1.2 on 2018-11-26 19:13

import ckeditor.fields
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_del_archivo', models.CharField(blank=True, max_length=200)),
                ('descripción', ckeditor.fields.RichTextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('número_de_caja', models.CharField(blank=True, max_length=200)),
                ('letras', models.CharField(blank=True, max_length=200)),
                ('legajos', models.CharField(blank=True, max_length=200)),
                ('fechas_extremas', models.CharField(blank=True, max_length=200)),
                ('volumen_en_metros_lineales', models.CharField(blank=True, max_length=200)),
                ('sistema_digital', models.CharField(blank=True, max_length=200)),
                ('descripción', ckeditor.fields.RichTextField(blank=True, default='')),
                ('archivo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gam_app.Archivo')),
            ],
        ),
        migrations.CreateModel(
            name='Carpeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carpeta_titulo', models.CharField(blank=True, max_length=200)),
                ('nombre_de_la_carpeta', models.CharField(blank=True, max_length=200)),
                ('caja', models.CharField(blank=True, max_length=200)),
                ('legajo', models.CharField(blank=True, max_length=200)),
                ('carpeta', models.CharField(blank=True, max_length=200)),
                ('número_de_víctimas', models.IntegerField(blank=True, null=True)),
                ('tipo_de_violencia', models.CharField(blank=True, max_length=200)),
                ('descripción', ckeditor.fields.RichTextField(blank=True, default='')),
                ('descripción_generada_automaticamente', ckeditor.fields.RichTextField(blank=True)),
                ('person_status', models.CharField(blank=True, choices=[('NONE', 'Sin correcciones'), ('IN', 'En progreso'), ('DONE', 'Compitió'), ('FINAL', 'Competido y verificado')], max_length=20, null=True)),
                ('place_status', models.CharField(blank=True, choices=[('NONE', 'Sin correcciones'), ('IN', 'En progreso'), ('DONE', 'Compitió'), ('FINAL', 'Competido y verificado')], max_length=20, null=True)),
                ('organization_status', models.CharField(blank=True, choices=[('NONE', 'Sin correcciones'), ('IN', 'En progreso'), ('DONE', 'Compitió'), ('FINAL', 'Competido y verificado')], max_length=20, null=True)),
                ('archivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gam_app.Archivo')),
            ],
        ),
        migrations.CreateModel(
            name='Caso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caso', models.CharField(blank=True, max_length=200)),
                ('fecha_desaparicion', models.CharField(blank=True, max_length=200)),
                ('departamento', models.CharField(blank=True, max_length=200)),
                ('local', models.CharField(blank=True, max_length=200)),
                ('area', models.CharField(blank=True, max_length=200)),
                ('ambiente', models.CharField(blank=True, max_length=200)),
                ('estanteria_no', models.CharField(blank=True, max_length=200)),
                ('plato_no', models.CharField(blank=True, max_length=200)),
                ('caja_no', models.CharField(blank=True, max_length=200)),
                ('legajo_no', models.CharField(blank=True, max_length=200)),
                ('carpeta_no', models.CharField(blank=True, max_length=200)),
                ('descripcion_caso', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='Colección',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_la_colección', models.CharField(blank=True, max_length=200)),
                ('descripción', ckeditor.fields.RichTextField(blank=True, default='')),
                ('archivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gam_app.Archivo')),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_del_archivo', models.CharField(blank=True, max_length=200)),
                ('localizacion_fisica', models.CharField(blank=True, max_length=200)),
                ('caja', models.CharField(blank=True, max_length=200)),
                ('legajo', models.CharField(blank=True, max_length=200)),
                ('carpeta', models.CharField(blank=True, max_length=200)),
                ('número_de_imagen', models.CharField(blank=True, max_length=200)),
                ('forma_de_GAM', models.CharField(blank=True, max_length=200)),
                ('texto_de_OCR', ckeditor.fields.RichTextField(blank=True)),
                ('notas', ckeditor.fields.RichTextField(blank=True)),
                ('traducción', ckeditor.fields.RichTextField(blank=True)),
                ('status', models.CharField(blank=True, choices=[('NONE', 'Sin correcciones'), ('IN', 'En progreso'), ('DONE', 'Compitió'), ('FINAL', 'Competido y verificado')], max_length=20)),
                ('bag_name', models.CharField(blank=True, max_length=200)),
                ('archivo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gam_app.Archivo')),
                ('colección', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gam_app.Colección')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_del_item', models.CharField(max_length=200, null=True)),
                ('site', models.ManyToManyField(to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_del_lugar', models.CharField(max_length=200, null=True)),
                ('punto', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('image', models.ManyToManyField(blank=True, to='gam_app.Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Organización',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_la_organización', models.CharField(max_length=200, null=True)),
                ('image', models.ManyToManyField(blank=True, to='gam_app.Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_la_persona', models.CharField(max_length=200, null=True)),
                ('nombre', models.CharField(blank=True, max_length=200)),
                ('segundo', models.CharField(blank=True, max_length=200)),
                ('apellido_paterno', models.CharField(blank=True, max_length=200)),
                ('apellido_materno', models.CharField(blank=True, max_length=200)),
                ('fecha_de_nacimiento', models.CharField(blank=True, max_length=200)),
                ('fecha_desaparicion', models.CharField(blank=True, max_length=200)),
                ('edad_en_el_momento', models.CharField(blank=True, max_length=200)),
                ('género', models.CharField(blank=True, max_length=200)),
                ('etnicidad', models.CharField(blank=True, max_length=200)),
                ('profesión', models.CharField(blank=True, max_length=200)),
                ('notas', ckeditor.fields.RichTextField(blank=True)),
                ('actividades_políticas', models.ManyToManyField(blank=True, to='gam_app.Organización')),
                ('image', models.ManyToManyField(blank=True, to='gam_app.Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Portapapeles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_del_portapapeles', models.CharField(blank=True, max_length=200)),
                ('casos', models.ManyToManyField(blank=True, to='gam_app.Caso')),
                ('imágenes', models.ManyToManyField(blank=True, to='gam_app.Imagen')),
                ('manuscrito', models.ManyToManyField(blank=True, to='gam_app.Item')),
                ('usuario', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relación',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relación', models.CharField(max_length=200, null=True)),
                ('persona_A', models.ManyToManyField(related_name='A', to='gam_app.Persona')),
                ('persona_B', models.ManyToManyField(related_name='B', to='gam_app.Persona')),
            ],
        ),
        migrations.CreateModel(
            name='Transcrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_del_archivo', models.CharField(max_length=200)),
                ('tiempo_modificado', models.DateTimeField()),
                ('texto_transcrito', ckeditor.fields.RichTextField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='imagen',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gam_app.Item'),
        ),
        migrations.AddField(
            model_name='carpeta',
            name='colección',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gam_app.Colección'),
        ),
        migrations.AddField(
            model_name='carpeta',
            name='organización',
            field=models.ManyToManyField(blank=True, to='gam_app.Organización'),
        ),
        migrations.AddField(
            model_name='carpeta',
            name='persona',
            field=models.ManyToManyField(blank=True, to='gam_app.Persona'),
        ),
        migrations.AddField(
            model_name='carpeta',
            name='ubicación_geográfica',
            field=models.ManyToManyField(blank=True, to='gam_app.Lugar'),
        ),
        migrations.AddField(
            model_name='caja',
            name='carpetas',
            field=models.ManyToManyField(blank=True, related_name='carpetas', to='gam_app.Carpeta'),
        ),
        migrations.AddField(
            model_name='caja',
            name='colección',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gam_app.Colección'),
        ),
        migrations.AddField(
            model_name='caja',
            name='departamento',
            field=models.ManyToManyField(blank=True, related_name='departamento', to='gam_app.Lugar'),
        ),
        migrations.AddField(
            model_name='caja',
            name='municipios',
            field=models.ManyToManyField(blank=True, related_name='municipios', to='gam_app.Lugar'),
        ),
    ]
