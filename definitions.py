import os
from tools.read_config import *

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONF_DIR = os.path.join(ROOT_DIR, 'conf')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
UTILS_DIR = os.path.join(ROOT_DIR, 'utils')
DRIVER_DIR = os.path.join(ROOT_DIR, 'driver-envs')


conf = initialize_config(os.path.join(CONF_DIR, 'config.ini'))

chromedriver_path = get_variable(conf, 'chromedriver_path', 'str', 'all')
linked_in_username = get_variable(conf, 'username', 'str', 'linked_in')
linked_in_password = get_variable(conf, 'password', 'str', 'linked_in')
job_search = get_variable(conf, 'job_search', 'str', 'all')
job_search_location = get_variable(conf, 'job_search_location', 'str', 'all')
