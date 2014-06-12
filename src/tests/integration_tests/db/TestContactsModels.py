"""Contacts app models component tests"""

from django.test import TestCase
from apps.contacts.models import Contact, Title
from apps.companies.models import Company
from apps.teams.models import Team


class ContactTests(TestCase):
	@classmethod 
	def setUpClass(cls):
		team = Team.objects.create(name="Team")
		cls.company = Company.objects.create(name="Company", team=team)
		cls.contact = Contact.objects.create(company=cls.company)


	@classmethod
	def tearDownClass(cls):
		flush = (Team, Contact, Company, Title)
		map(lambda x: getattr(x.objects, 'all')().delete(), flush)


	def test_contact_summary_returns_proper_contact_format(self):
		title = Title.objects.create(name="CEO")
		Contact.objects.filter(pk=1).update(title=title,
											first_name='Kevin',
											last_name='Hudson'
                                            )
		self.assertEqual(Contact.objects.get().get_summary(), '(CEO) Kevin Hudson')