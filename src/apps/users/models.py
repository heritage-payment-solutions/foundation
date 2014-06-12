from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.teams.models import Team
from apps.phones.models import Phone, CallCode


class Staff(models.Model):
    # Staff constants
    # --
    # @role
    MARKETER = _("Marketer")
    SALES_REP = _("Sales Rep")


    # Staff choices
    # --
    ROLE_CHOICES = (
        (0, MARKETER),
        (1, SALES_REP)
    )


    # Staff fields
    # --
    user = models.OneToOneField(User)
    role = models.IntegerField(
        choices=ROLE_CHOICES, 
        default=0,
        help_text=_("The role of the user.  Inside Marketer or Sales Rep")
    )
    teams = models.ManyToManyField(
        Team,
        related_name="staff",
        null=True, 
        blank=True
    )
    phone = models.ForeignKey(
        Phone, 
        null=True, 
        blank=True
    )
    call_codes = models.ManyToManyField(
        CallCode, 
        related_name="staff", 
        null=True, 
        blank=True
    )


    class Meta:
        verbose_name_plural = _("Staff")


    def __unicode__(self):
        return "%s %s" % (
            getattr(self.user, "first_name", None),
            getattr(self.user, "last_name", None)
        )


# Django Admin
class StaffAdmin(admin.ModelAdmin):
    pass


class StaffInline(admin.StackedInline):
    model = Staff
    can_delete = False
    verbose_name_plural = _("Staff settings")


class UserAdmin(UserAdmin):
    inlines = (StaffInline,)


admin.site.register(Staff, StaffAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)