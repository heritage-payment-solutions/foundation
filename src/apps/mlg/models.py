from django.db import models 
from django.contrib import admin
from apps.companies.models import Company


class MLG(models.Model):
	primary = models.ForeignKey(Company, 
		                        related_name='mlg_pri',
		                        null=True,
		                        blank=True
		                        )
	associates = models.ManyToManyField(Company,
		                                related_name='mlg_asc',
		                                null=True,
		                                blank=True
		                                )


	class Meta:
		verbose_name= 'Multi Location Group'
		verbose_name_plural = 'Multi Location Groups'


	def __unicode__(self):
		if getattr(self, 'primary', None) is not None:
			return self.primary.name
		else:
			# nps = no primary specified
			return "MLG -- %d associate(s)" % len(self.associates.all())


class MLGAdmin(admin.ModelAdmin):
	pass


admin.site.register(MLG, MLGAdmin)