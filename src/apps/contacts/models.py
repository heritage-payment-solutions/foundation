from django.db import models
from django.contrib import admin
from apps.companies.models import Company


class Title(models.Model):
    name = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    company = models.ForeignKey(Company, related_name='contacts')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    title = models.ForeignKey(Title, null=True, blank=True)


    def get_summary(self):
        """
        Return Contact in summary form "(CEO) Joe Schmoe"
        """

        # match empty string or None values and return none
        # if attribute has a value that is not None or empty string return value
        title, first, last = map(
        lambda x: None if getattr(self, x) == '' or getattr(self, x) == None 
            else getattr(self, x), ['title', 'first_name', 'last_name'])
        # set title to None if self.title is empty string to prevent returning 
        # '()' as title
        title = "(%s)" % title if title != None else None
        # filter over attrs and return value if it isn't None
        return ' '.join(filter(lambda x: x != None, 
            [title, first, last])).strip()


    def __unicode__(self):
        return "%s %s" % (getattr(self, 'first_name', None), 
                          getattr(self, 'last_name', None)
                          )


class ContactInfo(models.Model):
    company = models.ForeignKey(
        Company, 
        related_name='contact_infos'
    )  
    PHONE = 'Phone'
    EMAIL = 'Email'
    FAX = 'Fax'
    METHOD_CHOICES = (
        (0, PHONE),
        (1, EMAIL),
        (2, FAX)
    )
    method = models.IntegerField(
        max_length=1,
        choices=METHOD_CHOICES,
        help_text='The contact media type (ie. phone, email, etc.)'
    )
    OFFICE = 'Work'
    MOBILE = 'Mobile'
    TOLL_FREE = 'Toll Free'
    TYPE_CHOICES = (
        (0, OFFICE),
        (1, MOBILE),
        (2, TOLL_FREE)
    )
    type = models.IntegerField(max_length=1,
        null=True,
        blank=True,
        choices=TYPE_CHOICES,
        help_text='The contact location type (ie. work, mobile, etc.)',
    ) 
    info = models.CharField(max_length=100)


    def __unicode__(self):
        return getattr(self, 'info', None)


#Django Admin
class ContactAdmin(admin.ModelAdmin):
    pass


class ContactInfoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)