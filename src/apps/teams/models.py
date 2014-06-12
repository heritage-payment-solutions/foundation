from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Team(models.Model):
    user = models.ForeignKey(User, related_name='teams', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)


    def __unicode__(self):
        if self.name != '':
            return self.name
        if getattr(self, 'user', None) is not None:
            user = "%s%s" % (
                getattr(self, 'user.first_name', None),
                # convert last_name to str for space concatenation exception 
                # raised on NoneType returned from unset last_name of associated
                # user model
                ' ' + str(getattr(self, 'user.last_name', None))
            )
            # fallback to username if user first_name/last_name is not set
            return user if user != 'None None' else self.user.username


# Django Admin
class TeamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Team, TeamAdmin)