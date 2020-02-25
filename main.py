from tools.read_config import *

from objects.LinkedIn import LinkedInDriver





# Reading Config
################################################################################
################################################################################
################################################################################

conf = initialize_config()

chromedriver_path = get_variable(conf, 'chromedriver_path', 'str', 'all')
linked_in_username = get_variable(conf, 'username', 'str', 'linked_in')
linked_in_password = get_variable(conf, 'password', 'str', 'linked_in')
job_search = get_variable(conf, 'job_search', 'str', 'all')
job_search_location = get_variable(conf, 'job_search_location', 'str', 'all')

################################################################################
################################################################################
################################################################################

linked_in_driver = LinkedInDriver(linked_in_username = linked_in_username, linked_in_password = linked_in_password)
linked_in_driver.easy_apply(job_search, job_search_location)
