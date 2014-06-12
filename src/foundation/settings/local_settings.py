from settings import INSTALLED_APPS
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from vendor.utility import load_apps

# Libraries
APPS = (
	'suit',
	'django_nose'
)

# Model Modules
# APPS += apps.bootstrap(INSTALLED_APPS)
APPS += INSTALLED_APPS

INSTALLED_APPS = APPS

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'