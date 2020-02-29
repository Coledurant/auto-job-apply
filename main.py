from definitions import *
from objects.LinkedIn import LinkedInDriver
import os




################################################################################
################################################################################
################################################################################

linked_in_driver = LinkedInDriver(chromedriver_path = chromedriver_path, linked_in_username = linked_in_username, linked_in_password = linked_in_password)
linked_in_driver.easy_apply(job_search, job_search_location)
