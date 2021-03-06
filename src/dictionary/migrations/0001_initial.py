# Generated by Django 3.1.1 on 2020-12-17 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'dictionary',
                'verbose_name_plural': 'dictionaries',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('examples', models.TextField()),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('tagged_text', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('token_statistics', models.JSONField(null=True)),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='texts', to='dictionary.dictionary')),
            ],
        ),
        migrations.CreateModel(
            name='Lemma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lemmas', to='dictionary.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('frequency', models.BigIntegerField(default=0)),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='dictionary.dictionary')),
                ('lemma', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='token', to='dictionary.lemma')),
                ('tags', models.ManyToManyField(related_name='tokens', to='dictionary.Tag')),
            ],
            options={
                'ordering': ['-frequency'],
                'unique_together': {('label', 'dictionary')},
            },
        ),
    ]
