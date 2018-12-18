# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class CategoryOers(models.Model):
    name = models.CharField(max_length=175, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_oers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Downloads(models.Model):
    name = models.CharField(max_length=245, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    oer = models.ForeignKey('Oer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'downloads'


class Oer(models.Model):
    title = models.CharField(max_length=245, blank=True, null=True)
    author = models.CharField(max_length=445, blank=True, null=True)
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
    tags = models.CharField(max_length=375, blank=True, null=True)

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


class TypeOer(models.Model):
    name = models.CharField(max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_oer'
