import math
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import CONSTANTS
import config
import utils
from utils import print_red, print_yellow, print_green


def display_write_results(line_to_write: str):
    try:
        print(line_to_write)
        utils.write_results(line_to_write)
    except Exception as e:
        print_red("Error in DisplayWriteResults: " + str(e))


def generate_urls():
    if not os.path.exists('data'):
        os.makedirs('data')
    try:
        with open('data/urlData.txt', 'w', encoding="utf-8") as file:
            linkedin_job_links = utils.generate_url_links()
            for url in linkedin_job_links:
                file.write(url + "\n")
        print_green("Urls are created successfully, now the bot will visit those urls.")
    except:
        print_red(
            "Couldn't generate url, make sure you have /data folder and modified config.py file for your "
            "preferences.")


class Linkedin:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
            print_yellow("Trying to log in linkedin.")
        except Exception as e:
            print_red("Warning ChromeDriver" + str(e))

        try:
            self.driver.find_element("id", "username").send_keys(config.email)
            time.sleep(CONSTANTS.SLOW)
            self.driver.find_element("id", "password").send_keys(config.password)
            time.sleep(CONSTANTS.SLOW)
            self.driver.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button').click()
        except:
            print_red("Couldn't log in Linkedin.")

    def linkedin_job_apply(self):
        generate_urls()
        count_applied = 0
        count_jobs = 0

        url_data = utils.get_url_data_file()

        for url in url_data:
            self.driver.get(url)

            total_jobs = self.driver.find_element(By.XPATH, '//small').text
            total_pages = utils.jobs_to_pages(total_jobs)

            url_words = utils.url_to_keywords(url)
            line_to_write = "\n Category: " + url_words[0] + ", Location: " + url_words[1] + ", Applying " + str(
                total_jobs) + " jobs."

            display_write_results(line_to_write)

            for page in range(total_pages):
                current_page_jobs = CONSTANTS.jobs_per_page * page
                url = url + "&start=" + str(current_page_jobs)

                self.driver.get(url)
                time.sleep(random.uniform(1, CONSTANTS.botSpeed))

                offers_per_page = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')

                offer_ids = []
                for offer in offers_per_page:
                    offer_id = offer.get_attribute("data-occludable-job-id")
                    offer_ids.append(int(offer_id.split(":")[-1]))

                for job_id in offer_ids:
                    offer_page = 'https://www.linkedin.com/jobs/view/' + str(job_id)
                    self.driver.get(offer_page)
                    time.sleep(random.uniform(1, CONSTANTS.botSpeed))

                    count_jobs += 1

                    job_properties = self.get_job_properties(count_jobs)
                    if "blacklisted" in job_properties:
                        line_to_write = job_properties + " | " + "* 🤬 Blacklisted Job, skipped!: " + str(offer_page)
                        display_write_results(line_to_write)

                    else:
                        button = self.easy_apply_button()

                        if button is not False:
                            button.click()
                            time.sleep(random.uniform(1, CONSTANTS.botSpeed))
                            count_applied += 1
                            try:
                                self.driver.find_element(By.CSS_SELECTOR,
                                                         "button[aria-label='Submit application']").click()
                                time.sleep(random.uniform(1, CONSTANTS.botSpeed))

                                line_to_write = job_properties + " | " + "* 🥳 Just Applied to this job: " + str(
                                    offer_page)
                                display_write_results(line_to_write)

                            except:
                                try:
                                    self.driver.find_element(By.CSS_SELECTOR,
                                                             "button[aria-label='Continue to next step']").click()
                                    time.sleep(random.uniform(1, CONSTANTS.botSpeed))

                                    complete_percentage = self.driver.find_element(By.XPATH,
                                                                                   'html/body/div[3]/div/div/div['
                                                                                   '2]/div/div/span').text
                                    percent_number = int(complete_percentage[0:complete_percentage.index("%")])
                                    result = self.apply_process(percent_number, offer_page)
                                    line_to_write = job_properties + " | " + result
                                    display_write_results(line_to_write)

                                except Exception as e:
                                    line_to_write = job_properties + " | " + "* 🥵 Cannot apply to this Job! " + str(
                                        offer_page)
                                    display_write_results(line_to_write)

                        else:
                            line_to_write = job_properties + " | " + "* 🥳 Already applied! Job: " + str(offer_page)
                            display_write_results(line_to_write)

            print_yellow("Category: " + url_words[0] + "," + url_words[1] + " applied: " + str(count_applied) +
                         " jobs out of " + str(count_jobs) + ".")

    def get_job_properties(self, count):
        try:
            job_title = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job-title')]").get_attribute(
                "innerHTML").strip()
            res = [blacklist_item for blacklist_item in config.blacklist_Titles if
                   (blacklist_item.lower() in job_title.lower())]

            if len(res) > 0:
                job_title += "(blacklisted title: " + ' '.join(res) + ")"
        except Exception as e:
            print_yellow("Warning in getting jobTitle: " + str(e)[0:50])
            job_title = ""

        try:
            job_company = self.driver.find_element(By.XPATH,
                                                   "//a[contains(@class, 'ember-view t-black t-normal')]").get_attribute(
                "innerHTML").strip()
            res = [blacklist_item for blacklist_item in config.blacklist_Companies if
                   (blacklist_item.lower() in job_title.lower())]
            if len(res) > 0:
                job_company += "(blacklisted company: " + ' '.join(res) + ")"
        except Exception as e:
            print_yellow("Warning in getting jobCompany: " + str(e)[0:50])
            job_company = ""

        try:
            job_location = self.driver.find_element(By.XPATH, "//span[contains(@class, 'bullet')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print_yellow("Warning in getting jobLocation: " + str(e)[0:50])
            job_location = ""

        try:
            job_work_place = self.driver.find_element(By.XPATH,
                                                      "//span[contains(@class, 'workplace-type')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print_yellow("Warning in getting jobWorkPlace: " + str(e)[0:50])
            job_work_place = ""
        try:
            job_posted_date = self.driver.find_element(By.XPATH,
                                                       "//span[contains(@class, 'posted-date')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print_yellow("Warning in getting jobPostedDate: " + str(e)[0:50])
            job_posted_date = ""

        try:
            job_applications = self.driver.find_element(By.XPATH,
                                                        "//span[contains(@class, 'applicant-count')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print_yellow("Warning in getting jobApplications: " + str(e)[0:50])
            job_applications = ""

        text_to_write = str(
            count) + " | " + job_title + " | " + job_company + " | " + job_location + " | " + job_work_place + " | " + job_posted_date + " | " + job_applications

        return text_to_write

    def easy_apply_button(self):
        try:
            time.sleep(CONSTANTS.SLOW)
            button = self.driver.find_element(By.XPATH, '//button[contains(@class, "jobs-apply-button")]')
            easy_apply_button = button
        except:
            easy_apply_button = False

        return easy_apply_button

    def apply_process(self, percentage, offer_page):
        apply_pages = math.floor(100 / percentage)

        try:
            try:
                for pages in range(apply_pages - 2):
                    self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                    time.sleep(random.uniform(1, CONSTANTS.botSpeed))

                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Choose Resume']").click()
                time.sleep(random.uniform(1, CONSTANTS.botSpeed))

                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                time.sleep(random.uniform(1, CONSTANTS.botSpeed))
            except:
                pass

            try:
                for pages in range(apply_pages - 2):
                    self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                    time.sleep(random.uniform(1, CONSTANTS.botSpeed))
            except:
                pass

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
            time.sleep(random.uniform(1, CONSTANTS.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
            time.sleep(random.uniform(1, CONSTANTS.botSpeed))

            result = "* 🥳 Just Applied to this job: " + str(offer_page)

        except:
            result = "* 🥵 " + str(apply_pages) + " Pages, couldn't apply to this job! Extra info needed. Link: " + str(
                offer_page)

        return result
