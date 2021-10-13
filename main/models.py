from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):
    event = models.ForeignKey('Event', models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
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
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        managed = True
        db_table = 'szakal_categories'


class CategoryCompany(models.Model):
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
    name = models.TextField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    www = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    insert_date = models.DateTimeField()
    update_date = models.DateTimeField()
    update_person_name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
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
    contact_person = models.ForeignKey('ContactPerson', models.DO_NOTHING)
    type = models.ForeignKey('ContactType', models.DO_NOTHING)
    event = models.ForeignKey('Event', models.DO_NOTHING)
    status = models.ForeignKey('Status', models.DO_NOTHING)
    company = models.ForeignKey('Company', models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
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
    name = models.CharField(max_length=20)
    local = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        managed = True
        db_table = 'szakal_events'


class Industry(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
        managed = True
        db_table = 'szakal_industries'


class IndustryCompany(models.Model):
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
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact Type'
        verbose_name_plural = 'Contact Types'
        managed = True
        db_table = 'szakal_types'
