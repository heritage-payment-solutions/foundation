# Companies Component Tests

from django.test import TestCase
from apps.teams.models import Team
from apps.mlg.models import MLG
from apps.companies.models import Company


class CompaniesComponentTests(TestCase):
	@classmethod
	def setUpClass(cls):
		team = Team.objects.create(name="Team")
		cls.company = Company.objects.create(name="Company", team=team, mlg_status=0)
		MLG.objects.create()


	@classmethod
	def tearDownClass(cls):
		flush = (Team, MLG, Company)
		map(lambda x: getattr(x.objects, 'all')().delete(), flush)

	
	def test_company_get_mlg_primary_returns_None_if_no_primary_is_set(self):
		self.assertTrue(self.company.get_mlg_primary() is None)


	def test_company_get_mlg_primary_returns_company_instance_if_primary_is_set(self):
		MLG.objects.all().update(primary=self.company)
		self.assertEqual(self.company.get_mlg_primary().id, self.company.id)