from django.db import models 
from django.contrib import admin
from django.contrib.auth.models import User 
from apps.companies.models import Company
from apps.tasks.models import Task


class Note(models.Model):
	user = models.ForeignKey(User, related_name='notes')
	company = models.ForeignKey(Company, related_name='notes')
	task = models.ForeignKey(Task, related_name='notes')
	created_on = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=500)


	def __unicode__(self):
		return self.text


class NotePreset(models.Model):
	text = models.CharField(max_length=25)

	def __unicode__(self):
		return self.text


class NotePresetAdmin(admin.ModelAdmin):
	pass


admin.site.register(NotePreset, NotePresetAdmin)