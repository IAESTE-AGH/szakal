from django.db import models


class Assignment(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.ForeignKey('Event', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    company = models.ForeignKey('Company', models.DO_NOTHING)
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
    category = models.ForeignKey('Category', models.DO_NOTHING)
    company = models.ForeignKey('Company', models.DO_NOTHING)

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
    company = models.ForeignKey('Company', models.DO_NOTHING)
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
    contact_person = models.ForeignKey('ContactPerson', models.DO_NOTHING)
    type = models.ForeignKey('ContactType', models.DO_NOTHING)
    event = models.ForeignKey('Event', models.DO_NOTHING)
    status = models.ForeignKey('Status', models.DO_NOTHING)
    company = models.ForeignKey('Company', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
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
    industry = models.ForeignKey('Industry', models.DO_NOTHING)
    company = models.ForeignKey('Company', models.DO_NOTHING)

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
