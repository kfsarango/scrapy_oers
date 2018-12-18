# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CategoryOers(models.Model):
    name = models.CharField(max_length=175, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_oers'
    def __unicode__(self):
        return '%s | %s' % (self.id, self.name)


class Downloads(models.Model):
    name = models.CharField(max_length=245, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    oer = models.ForeignKey('Oer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'downloads'

class Oer(models.Model):
    title = models.CharField(max_length=545, blank=True, null=True)
    author = models.CharField(max_length=745, blank=True, null=True)
    subjects = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    education_level = models.CharField(max_length=245, blank=True, null=True)
    license = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    download_link = models.TextField(blank=True, null=True)
    type_oer = models.ForeignKey('TypeOer', models.DO_NOTHING)
    pages = models.ForeignKey('Pages', models.DO_NOTHING)
    category_oers = models.ForeignKey(CategoryOers, models.DO_NOTHING)
    source = models.TextField(blank=True, null=True)
    number = models.CharField(max_length=345, blank=True, null=True)
    identifier = models.CharField(max_length=345, blank=True, null=True)
    recommended_citation = models.TextField(blank=True, null=True)
    publication_date = models.CharField(max_length=145, blank=True, null=True)
    publisher = models.CharField(max_length=345, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    material_type = models.CharField(max_length=245, blank=True, null=True)
    provider = models.CharField(max_length=345, blank=True, null=True)
    set_provider = models.CharField(max_length=345, blank=True, null=True)
    grades = models.CharField(max_length=445, blank=True, null=True)
    language = models.CharField(max_length=245, blank=True, null=True)
    media_format = models.CharField(max_length=245, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oer'


class Pages(models.Model):
    name = models.CharField(max_length=145, blank=True, null=True)
    domain = models.CharField(max_length=145, blank=True, null=True)
    link_site = models.CharField(max_length=445, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pages'
    def __unicode__(self):
    	return "%s | %s | %s | %s" % (self.id, self.name, self.domain, self.link_site)


class TypeOer(models.Model):
    name = models.CharField(max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_oer'
    def __unicode__(self):
    	return "%s | %s" % (self.id, self.name)
