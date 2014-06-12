"""Utility function unit tests"""

import os

from unittest import TestCase
from vendor.utility import load_apps

class TestLoadApps(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.mock_apps = ("app1", "app3")
		cls.mock_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock', 'mock_apps_dir')
		cls.module_prefix = "mock_apps"


	def test_load_apps_returns_tuple(self):
		apps = load_apps(self.mock_apps, self.mock_dir, self.module_prefix)
		self.assertTrue(isinstance(apps, tuple))


	def test_load_apps_returns_specified_apps(self):
		apps = load_apps(self.mock_apps, self.mock_dir, self.module_prefix)
		self.assertTrue("{}.app1".format(self.module_prefix) in apps)
		self.assertTrue("{}.app2".format(self.module_prefix) in apps)