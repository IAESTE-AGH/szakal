# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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


class Assignments(models.Model):
    event = models.OneToOneField('Events', models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    company = models.ForeignKey('Companies', models.DO_NOTHING)
    active = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f'{self.event.name} - {self.company.name}'

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        managed = False
        db_table = 'assignments'
        unique_together = (('event', 'user', 'company'),)


class Categories(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        managed = False
        db_table = 'categories'


class CategoriesCompanies(models.Model):
    category = models.OneToOneField(Categories, models.DO_NOTHING, primary_key=True)
    company = models.ForeignKey('Companies', models.DO_NOTHING)

    def __str__(self):
        return f'{self.category.name} - {self.company.name}'

    class Meta:
        verbose_name_plural = 'CategoriesCompanies'
        managed = False
        db_table = 'categories_companies'
        unique_together = (('category', 'company'),)


class Companies(models.Model):
    company_id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    www = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    insert_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user_id = models.IntegerField(blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    number_of_ratings = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        managed = False
        db_table = 'companies'


class ContactPersons(models.Model):
    contact_person_id = models.IntegerField(primary_key=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING)
    name = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=75, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.company} - {self.name}'

    class Meta:
        verbose_name_plural = 'ContactPersons'
        managed = False
        db_table = 'contact_persons'


class Contacts(models.Model):
    contact_id = models.IntegerField(primary_key=True)
    contact_person = models.ForeignKey(ContactPersons, models.DO_NOTHING)
    type = models.ForeignKey('Types', models.DO_NOTHING)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    status = models.ForeignKey('Statuses', models.DO_NOTHING)
    company = models.ForeignKey(Companies, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    accepted = models.BooleanField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.company.name} - {self.event.name}'

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        managed = False
        db_table = 'contacts'


class Events(models.Model):
    event_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        managed = False
        db_table = 'events'


class Industries(models.Model):
    industry_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
        managed = False
        db_table = 'industries'


class IndustriesCompanies(models.Model):
    industry = models.OneToOneField(Industries, models.DO_NOTHING, primary_key=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING)

    def __str__(self):
        return f'{self.industry.name} - {self.company.name}'

    class Meta:
        verbose_name_plural = 'IndustriesCompanies'
        managed = False
        db_table = 'industries_companies'
        unique_together = (('industry', 'company'),)


class Statuses(models.Model):
    status_id = models.IntegerField(primary_key=True)
    sort_order = models.IntegerField()
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
        managed = False
        db_table = 'statuses'


class Types(models.Model):
    type_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'
        managed = False
        db_table = 'types'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.TextField()
    name = models.CharField(max_length=25, blank=True, null=True)
    surname = models.CharField(max_length=25, blank=True, null=True)
    working_group = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    logins = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    accepted = models.BooleanField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
