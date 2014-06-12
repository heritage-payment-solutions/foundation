from django.db import models
from django.contrib import admin


class Phone(models.Model):
    ip = models.CharField(max_length=15)
    port = models.IntegerField(max_length=5, null=True, blank=True)


    def __unicode__(self):
        return "%s%s" % (
            getattr(self, 'ip', None), 
            ":%s" % self.port if getattr(self, 'port', None) is not None else ''
        )


class CallCode(models.Model):
    code = models.IntegerField(max_length=5)
    map_area_code = models.IntegerField(max_length=3, null=True, blank=True)


    def __unicode__(self):
        return getattr(self, 'code', None)


class AreaCode(models.Model):
    area_code = models.IntegerField(max_length=3)
    map_area_code = models.IntegerField(max_length=3, null=True, blank=True)


    def __unicode__(self):
        return getattr(self, 'area_code', None)


# Django Admin
class PhoneAdmin(admin.ModelAdmin):
    pass


class CallCodeAdmin(admin.ModelAdmin):
    pass


class AreaCodeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Phone, PhoneAdmin)
admin.site.register(CallCode, CallCodeAdmin)
admin.site.register(AreaCode, AreaCodeAdmin)