from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from apps.teams.models import Team


class Profile(models.Model):
    name = models.CharField(max_length=50)
    sic_code = models.CharField(
        max_length=10, 
        null=True, 
        blank=True
    )


    def __unicode__(self):
        return getattr(self, "name", None)


class Tag(models.Model):
    name = models.CharField(max_length=50)


    def __unicode__(self):
        return getattr(self, "name", None)


class ListPriority(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name="priorities",
    )
    start = models.TimeField(
        null=True,
        blank=True
    )
    end = models.TimeField(
        null=True,
        blank=True
    )


    class Meta:
        verbose_name_plural=_("List priorities")


    def time_range(self):
        """
        Get the time range of the current list priority object.
        """
        return "%s * %s" % (
            self.start.strftime("%I:%M %p") 
                if getattr(self, "start", None) else "",
            self.end.strftime("%I:%M %p") 
                if getattr(self, "end", None) else ""
        )

    def associated_tags(self):
        """
        Return a string representation of the assocated tag objects of the list
        object.
        """
        return ", ".join(map(lambda x: x.name, self.tags.all()))


    def __unicode__(self):
        return self.time_range()



class Batch(models.Model):
    def __unicode__(self):
        return self.id


class Company(models.Model):
    # Company constants
    # --
    # @employee_count
    LT_TEN = _("Less Than 10")
    LT_FIFTY = _("Less Than 50")
    LT_ONE_HUNDRED = _("Less Than 100")
    LT_TWO_HUNDRED_FIFTY = _("Less Than 250")
    LT_FIVE_HUNDRED = _("Less Than 500")

    # @sales_volume
    LT_FIVE_HUNDRED_THOUSAND = _("Less than 500,000")
    LT_ONE_MILLION = _("Less than 1,000,000")
    LT_TWO_POINT_FIVE_MILLION = _("Less than 2,500,000")
    LT_TEN_MILLION = _("Less than 10,000,000")
    LT_FIFTY_MILLION = _("Less than 50,000,000")

    # @availbility
    OPEN = _("Open")
    LIMITED = _("Limited")
    RESTRICTED = _("Restricted")

    # @status
    ACTIVE = _("Active")
    PENDING = _("Pending")
    ARCHIVED = _("Archived")

    # @origin
    LEAD = _("Lead")
    COLDCALL = _("Cold Call")
    REFERRAL = _("Referral")

    # @mlg status
    FLAGGED = _("flagged")
    VERIFIED = _("verified")
    DECLINED = _("declined")


    # Company choices
    # --
    EMPLOYEE_COUNT_CHOICES = (
        (LT_TEN, -10),
        (LT_FIFTY, -50),
        (LT_ONE_HUNDRED, -100),
        (LT_TWO_HUNDRED_FIFTY, -250),
        (LT_FIVE_HUNDRED, -500),
    )
    SALES_VOLUME_CHOICES = (
        (LT_FIVE_HUNDRED_THOUSAND, -500000),
        (LT_ONE_MILLION, -1000000),
        (LT_TWO_POINT_FIVE_MILLION, -2500000),
        (LT_TEN_MILLION, -10000000),
        (LT_FIFTY_MILLION, -50000000)
    )
    AVAILABILITY_CHOICES = (
        (0, OPEN),
        (1, LIMITED),
        (2, RESTRICTED)
    )
    STATUS_CHOICES = (
        (0, ACTIVE),
        (1, PENDING),
        (2, ARCHIVED)
    )
    ORIGIN_CHOICES = (
        (0, COLDCALL),
        (1, LEAD),
        (2, REFERRAL)
    )
    MLG_STATUS_CHOICES = (
        (0, FLAGGED),
        (1, VERIFIED),
        (2, DECLINED)
    )


    # Company fields
    # --
    team = models.ForeignKey(Team, related_name="companies")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    address = models.CharField(
        max_length=100, 
        null=True, 
        blank=True
    )
    address2 = models.CharField(
        max_length=50, 
        null=True, 
        blank=True
    )
    city = models.CharField(
        max_length=50, 
        null=True, 
        blank=True
    )
    state = models.CharField(
        max_length=2,
        null=True, 
        blank=True
    )
    zipcode = models.CharField(
        max_length=10, 
        null=True, 
        blank=True
    )
    employee_count = models.IntegerField(
        null=True, 
        blank=True, 
        choices=EMPLOYEE_COUNT_CHOICES
    )
    sales_volume = models.IntegerField(
        null=True, 
        blank=True, 
        choices=SALES_VOLUME_CHOICES
    )
    profile = models.ForeignKey(
        Profile, 
        related_name="companies",
        null=True, 
        blank=True
    )
    availablity = models.IntegerField(
        max_length=1, 
        default=0, 
        choices=AVAILABILITY_CHOICES
    )
    available_from = models.DateTimeField(
        null=True, 
        blank=True
    )
    available_to = models.DateTimeField(
        null=True, 
        blank=True
    )
    comments = models.CharField(
        max_length=500, 
        null=True, 
        blank=True
    )
    status = models.IntegerField(
        max_length=1, 
        default=0,
        choices=STATUS_CHOICES
    )
    tags = models.ManyToManyField(
        Tag, 
        related_name="companies", 
        null=True, 
        blank=True
    )
    infousa_url = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )
    origin = models.IntegerField(
        max_length=1, 
        choices=ORIGIN_CHOICES, 
        default=0
    )
    batch = models.ForeignKey(
        Batch,
        related_name="companies",
        null=True, 
        blank=True,
        help_text=_("Upload batch number if company is created via list import")
    )
    mlg_status = models.IntegerField(max_length=1,
        null=True, 
        blank=True,
        choices=MLG_STATUS_CHOICES
    )


    class Meta:
        verbose_name_plural = "Companies"


    def get_mlg_primary(self):
        """
        Return current company's muliple location group primary if mlg exists.
        """
        try:
            return self.mlg_pri.get()
        except ObjectDoesNotExist:
            return None


    def get_mlg_associates(self):
        """
        Return current company's multiple location group associates.  Returns 
        empty array if there are no associates.
        """
        return self.mlg_asc


    def __unicode__(self):
        return getattr(self, "name", None)


#Django Admin
class ProfileAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


class ListPriorityAdmin(admin.ModelAdmin):
    list_display = [
        "associated_tags",
        "time_range"
    ]


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ListPriority, ListPriorityAdmin)
admin.site.register(Company, CompanyAdmin)