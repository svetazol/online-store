import os
import re
import sys
from distutils.util import strtobool

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = False
DEV = False

BASE_URL = ""

STATIC_URL = ""
STATIC_DIR = ""

PROJECT_HOST = None
PROJECT_PORT = 8082
PROJECT_SCHEMA = 'http'

DATABASE_URL = None
DATABASE_ENGINE = "postgresql+asyncpg"
DATABASE_HOST = None
DATABASE_PORT = None
DATABASE_NAME = None
DATABASE_USER = None
DATABASE_PASSWORD = None

_ENVIRONMENT_SETTINGS_PREFIX = "OS_"

try:
    from backend.settings.local import *  # noqa
except ImportError:
    pass
###############################################################################
#  Reset from environment
###############################################################################

current_module = sys.modules[__name__]
some_setting = re.compile("^[_A-Z]+$")
redefined_variables = []
for key in sorted((k for k in os.environ)):
    setting_value = os.getenv(key, None)
    if not key.startswith(_ENVIRONMENT_SETTINGS_PREFIX):
        continue
    setting_name = key[len(_ENVIRONMENT_SETTINGS_PREFIX):]
    if not hasattr(current_module, setting_name):
        continue
    # check old value, if it was bool or int - cast environment value
    setting_old_value = getattr(current_module, setting_name)
    if isinstance(setting_old_value, bool):
        setting_value = strtobool(setting_value)
    if isinstance(setting_old_value, int):
        setting_value = int(setting_value)
    redefined_variables.append('Define %s from environment, new value %s'
                               % (setting_name, setting_value))
    setattr(current_module, setting_name, setting_value)

if DEBUG:
    print('\n'.join(redefined_variables))

if not DATABASE_URL:
    DATABASE_URL = "{engine}://{username}:{password}@{host}:{port}/{name}".format(
        engine=DATABASE_ENGINE,
        username=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        name=DATABASE_NAME
    )
