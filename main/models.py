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


class Assignment(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    company = models.ForeignKey('Companies', models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.event.name} - {self.company.name}'

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        managed = True
        db_table = 'szakal_assignments'
        unique_together = (('event', 'user', 'company'),)


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        managed = True
        db_table = 'szakal_categories'


class CategoryCompany(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey('Categories', models.DO_NOTHING)
    company = models.ForeignKey('Companies', models.DO_NOTHING)

    def __str__(self):
        return f'{self.category.name} - {self.company.name}'

    class Meta:
        verbose_name_plural = 'Categories Companies'
        managed = True
        db_table = 'szakal_categories_companies'
        unique_together = (('category', 'company'),)


class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    www = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    insert_date = models.DateTimeField()
    update_date = models.DateTimeField()
    update_user_id = models.IntegerField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    delete_date = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    number_of_ratings = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        managed = True
        db_table = 'szakal_companies'


class ContactPerson(models.Model):
    id = models.IntegerField(primary_key=True)
    company = models.ForeignKey('Companies', models.DO_NOTHING)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=75)
    position = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.company} - {self.name}'

    class Meta:
        verbose_name_plural = 'Contact Persons'
        managed = True
        db_table = 'szakal_contact_persons'


class Contact(models.Model):
    id = models.IntegerField(primary_key=True)
    contact_person = models.ForeignKey('ContactPersons', models.DO_NOTHING)
    type = models.ForeignKey('ContactTypes', models.DO_NOTHING)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    status = models.ForeignKey('Statuses', models.DO_NOTHING)
    company = models.ForeignKey('Companies', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    accepted = models.BooleanField()
    last_update = models.DateTimeField()
    date = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.company.name} - {self.event.name}'

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        managed = True
        db_table = 'szakal_contacts'


class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        managed = True
        db_table = 'szakal_events'


class Industry(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
        managed = True
        db_table = 'szakal_industries'


class IndustryCompany(models.Model):
    id = models.IntegerField(primary_key=True)
    industry = models.ForeignKey('Industries', models.DO_NOTHING)
    company = models.ForeignKey('Companies', models.DO_NOTHING)

    def __str__(self):
        return f'{self.industry.name} - {self.company.name}'

    class Meta:
        verbose_name_plural = 'Industries Companies'
        managed = True
        db_table = 'szakal_industries_companies'
        unique_together = (('industry', 'company'),)


class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
        managed = True
        db_table = 'szakal_statuses'


class ContactType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact Type'
        verbose_name_plural = 'Contact Types'
        managed = True
        db_table = 'szakal_types'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.TextField()
    name = models.CharField(max_length=25, blank=True, null=True)
    surname = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    working_group = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    logins = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    accepted = models.BooleanField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        managed = True
        db_table = 'szakal_users'
