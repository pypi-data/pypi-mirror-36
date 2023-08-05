# Generated by Django 1.10.3 on 2016-11-26 16:02
from __future__ import unicode_literals

from django.db import migrations


def add_tilelayer(apps, *args):
    TileLayer = apps.get_model('umap', 'TileLayer')
    if TileLayer.objects.count():
        return
    TileLayer(
        name='Positron',
        url_template=('https://cartodb-basemaps-{s}.global.ssl.fastly.net/'
                      'light_all/{z}/{x}/{y}.png'),
        attribution=('&copy; [[http://www.openstreetmap.org/copyright|'
                     'OpenStreetMap]] contributors, &copy; '
                     '[[https://carto.com/attributions|CARTO]]')).save()


class Migration(migrations.Migration):

    dependencies = [
        ('umap', '0002_tilelayer_tms'),
    ]

    operations = [
        migrations.RunPython(add_tilelayer),
    ]
