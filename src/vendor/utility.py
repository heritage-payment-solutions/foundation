import os
import re

def load_apps(dj_apps, apps_dir, module_prefix="apps"):
    """Dynamically load Django project apps"""

    apps = filter(lambda x: not re.match(r'.*\.pyc|.*\.py', x), 
                  [app for app in os.listdir(apps_dir)]
                  )
    return tuple(["{}.{}".format(module_prefix, app) for app in apps])