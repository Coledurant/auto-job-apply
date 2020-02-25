from collections import namedtuple
from selenium.webdriver.common.keys import Keys
from functools import wraps
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import time

# Driver imports
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

Button = namedtuple('Button', ['button_name', 'button_class'])

important_button_classes = {
    'jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view' : 'easy apply',
    'artdeco-button artdeco-button--2 artdeco-button--primary ember-view' : 'review',
    'mr2 artdeco-button artdeco-button--2 artdeco-button--tertiary ember-view' : 'back',
    'artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--primary ember-view' : 'discard',
    'artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--secondary ember-view' : 'cancel',
    'search-s-facet__button artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--2 artdeco-button--secondary ember-view' : 'LinkedIn Features',
    'artdeco-button artdeco-button--2 artdeco-button--primary ember-view' : 'submit',
    'artdeco-button artdeco-button--2 artdeco-button--primary ember-view' : 'continue',
}

important_button_classes_reversed = {b:a for a, b in important_button_classes.items()}



class LinkedInDriver(object):

    def __init__(self, linked_in_username, linked_in_password, headless = False):

        self.linked_in_username = linked_in_username
        self.linked_in_password = linked_in_password

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options,executable_path="/Users/coledurant/Desktop/Other/PML/chromedriver.exe")
        options = Options()

        self.driver = driver

        self.linkedin_log_in()


    def linkedin_log_in(self, sleep_amount = 0):

        print("Logging into LinkedIn page...")

        self.driver.get('https://www.linkedin.com/login')

        time.sleep(sleep_amount)


        username = self.driver.find_element_by_id("username")
        password = self.driver.find_element_by_id("password")

        username.send_keys(self.linked_in_username)
        password.send_keys(self.linked_in_password)

        log_in_button = self.driver.find_element_by_xpath("//button[@class='btn__primary--large from__button--floating']")
        log_in_button.click()

        return None


    def press_button(self, button_class):

        button_obj = self.driver.find_element_by_xpath("//button[@class='{}']".format(important_button_classes_reversed.get(button_class)))
        button_obj.click()


    def find_next_button(self, **kwargs):

        buttons = self.find_buttons_on_page()

        button_names = [btn.button_name for btn in buttons]

        if 'pressed_buttons' in list(kwargs.keys()):

            for btn in kwargs.get('pressed_buttons'):

                if btn in button_names:

                    button_names.remove(btn)

                else:pass

        submitted = False

        if 'easy apply' in button_names:
            self.press_button('easy apply')
            pressed = 'easy apply'

        elif 'continue' in button_names:
            self.press_button('continue')

            time.sleep(1)

            # If there is another next button, dont take away this choice to press next time
            if 'continue' in [btn.button_name for btn in self.find_buttons_on_page()]:

                pressed = None

            else:

                pressed = 'continue'

        elif 'review' in button_names:
            self.press_button('review')
            pressed = 'review'

        elif 'submit' in button_names:
            self.press_button('submit')
            pressed = 'submit'
            submitted = True

        else:

            print('\n\n{}\n\n'.format(button_names))
            pressed = None
            return True

        return submitted, pressed



    def check_for_invalid_form_answer(self):

        '''
        For some of the easy apply applications there may be needed answers and this will check for that
        before looking for the next or submit button to hit
        '''

        driver_soup = BeautifulSoup(self.driver.page_source, 'lxml')

        invalid_pars = driver_soup.findAll('p', attrs={'class':'fb-form-element__error-text t-12'})

        if len(invalid_pars) > 0:

            for span in driver_soup.findAll('span', attrs={'class':"t-14 fb-form-element-label__title--is-required"}):

                print(span.text)
                print(link)
                print('\n')
            # form was invalid
            return True

        else:

            # form was valid
            return False



    def continue_to_next_step(self):

        next_not_available = False

        while not next_not_available:

            try:

                if self.check_for_invalid_form_answer():
                    return False


                next_button = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step']")
                next_button.click()


            except Exception as e:
                print(e)
                print('NEXT NOT AVAIL')
                next_not_available = True


        return True



    def find_buttons_on_page(self):

        '''
        A function used to find any important buttons on the current driver page
        '''


        driver_soup = BeautifulSoup(self.driver.page_source, 'lxml')

        buttons = driver_soup.findAll('button')

        buttons_on_current_page = [button for button in buttons if " ".join(button['class']) in list(important_button_classes.keys())]

        buttons_on_current_page_dict = [Button(important_button_classes.get(" ".join(button['class'])), button) for button in buttons_on_current_page]

        return buttons_on_current_page_dict


    def search_for_jobs(self, job_search_str = 'Quantitative Analyst', job_location_str = 'Chicago, Illinois, United States'):

        '''
        This is used to bring the driver to the LinkedIn search page of the job_search_str keyword and the job_location_str
        location.

        Parameters:
            job_search_str (str): A string to search jobs about
            job_location_str (str): A string for where to search for jobs
        '''

        self.driver.get('https://www.linkedin.com/jobs/')


        job_search_field = self.driver.find_element_by_id("jobs-search-box-keyword-id-ember32")
        job_location_field = self.driver.find_element_by_id("jobs-search-box-location-id-ember32")

        job_search_field.send_keys(job_search_str)
        job_location_field.send_keys(job_location_str)

        job_location_field.send_keys(Keys.RETURN)

        print("Job search for {} in {} has been completed...".format(job_search_str, job_location_str))

        return None


    def easy_apply(self, job_search_str = 'Quantitative Analyst', job_location_str = 'Chicago, Illinois, United States'):

        # Running the search on LinkedIn
        self.search_for_jobs(job_search_str, job_location_str)

        time.sleep(2)


        url = self.driver.current_url
        only_easy_apply_url = 'https://www.linkedin.com/jobs/search/' + '?f_LF=f_AL&' + url.split('https://www.linkedin.com/jobs/search/?')[1]

        self.driver.get(only_easy_apply_url)

        time.sleep(3)

        # Getting the linked of all the jobs with easy apply
        job_links = ['https://www.linkedin.com' + link['href'] for link in BeautifulSoup(self.driver.page_source, 'lxml').findAll('a', attrs={'class':'job-card-search__link-wrapper js-focusable disabled ember-view'})]




        for link in job_links:

            self.driver.get(link)

            time.sleep(2)

            buttons_on_page = self.find_buttons_on_page()

            if 'easy apply' in [btn.button_name for btn in buttons_on_page]:

                print("\nApplying to\n{}".format(link))

                submitted = False

                pressed_buttons = []


                while submitted != True:

                    #time.sleep(1)

                    try:
                        submitted, btn_pressed = self.find_next_button(pressed_buttons = pressed_buttons)
                        pressed_buttons.append(btn_pressed)
                    except TypeError:
                        submitted = True







            else:

                print("\nAlready applied to\n{}...".format(link))
