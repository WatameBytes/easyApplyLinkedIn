import CONSTANTS
import config
import math
import time
from typing import List


def print_red(prt):
    print(f"\033[91m{prt}\033[00m")


def print_green(prt):
    print(f"\033[92m{prt}\033[00m")


def print_yellow(prt):
    print(f"\033[93m{prt}\033[00m")


def get_url_data_file():
    url_data_url_data = ""
    try:
        file = open('data/urlData.txt', 'r')
        url_data_url_data = file.readlines()
    except FileNotFoundError:
        text = "FileNotFound:urlData.txt file is not found. Please run ./data folder exists and check config.py " \
               "values of yours. Then run the bot again "
        print_red(text)
    return url_data_url_data


def jobs_to_pages(num_of_jobs: str) -> int:
    if ' ' in num_of_jobs:
        space_index = num_of_jobs.index(' ')
        total_jobs = (num_of_jobs[0:space_index])
        total_jobs_int = int(total_jobs.replace(',', ''))
        number_of_pages = math.ceil(total_jobs_int / CONSTANTS.jobs_per_page)
        if number_of_pages > 40: number_of_pages = 40

    else:
        number_of_pages = int(num_of_jobs)

    return number_of_pages


def url_to_keywords(url: str) -> List[str]:
    keyword_url = url[url.index("keywords=") + 9:]
    keyword = keyword_url[0:keyword_url.index("&")]
    location_url = url[url.index("location=") + 9:]
    location = location_url[0:location_url.index("&")]
    return [keyword, location]


def write_results(text: str):
    time_str = time.strftime("%Y%m%d")
    file_name = "Applied Jobs DATA - " + time_str + ".txt"

    try:
        with open("data/" + file_name, encoding="utf-8") as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)

        with open("data/" + file_name, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + time_str + "\n")
            f.write(
                "---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result " + "\n")
            for line in lines:
                f.write(line)
            f.write(text + "\n")

    except:
        with open("data/" + file_name, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + time_str + "\n")
            f.write(
                "---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result " + "\n")

            f.write(text + "\n")


def print_info_message(bot: str):
    print_yellow("ℹ️ " + bot + " is starting soon... ")


def check_job_location(job):
    job_loc = "&location=" + job

    match job.casefold():
        case "Asia":
            job_loc += "&geoId=102393603"
        case "Europe":
            job_loc += "&geoId=100506914"
        case "NorthAmerica":
            job_loc += "&geoId=102221843&"
        case "SouthAmerica":
            job_loc += "&geoId=104514572"
        case "Australia":
            job_loc += "&geoId=101452733"
        case "Africa":
            job_loc += "&geoId=103537801"

    return job_loc


def job_experience():
    job_exp_array = config.experience_Levels
    first_job_exp = job_exp_array[0]
    job_exp = ""

    match first_job_exp:
        case "Internship":
            job_exp = "&f_E=1"
        case "Entry level":
            job_exp = "&f_E=2"
        case "Associate":
            job_exp = "&f_E=3"
        case "Mid-Senior level":
            job_exp = "&f_E=4"
        case "Director":
            job_exp = "&f_E=5"
        case "Executive":
            job_exp = "&f_E=6"

    for index in range(1, len(job_exp_array)):
        match job_exp_array[index]:
            case "Internship":
                job_exp += "%2C1"
            case "Entry level":
                job_exp += "%2C2"
            case "Associate":
                job_exp += "%2C3"
            case "Mid-Senior level":
                job_exp += "%2C4"
            case "Director":
                job_exp += "%2C5"
            case "Executive":
                job_exp += "%2C6"

    return job_exp


def job_type():
    job_type_array = config.job_Type
    first_job_type = job_type_array[0]
    job_type = ""

    match first_job_type:
        case "Full-time":
            job_type = "&f_JT=F"
        case "Part-time":
            job_type = "&f_JT=P"
        case "Contract":
            job_type = "&f_JT=C"
        case "Temporary":
            job_type = "&f_JT=T"
        case "Volunteer":
            job_type = "&f_JT=V"
        case "Internship":
            job_type = "&f_JT=I"
        case "Other":
            job_type = "&f_JT=O"

    for index in range(1, len(job_type_array)):
        match job_type_array[index]:
            case "Full-time":
                job_type += "%2CF"
            case "Part-time":
                job_type += "%2CP"
            case "Contract":
                job_type += "%2CC"
            case "Temporary":
                job_type += "%2CT"
            case "Volunteer":
                job_type += "%2CV"
            case "Internship":
                job_type += "%2CI"
            case "Other":
                job_type += "%2CO"

    job_type += "&"
    return job_type


def remote():
    remote_array = config.remote
    first_job_remote = remote_array[0]
    job_remote = ""
    match first_job_remote:
        case "On-site":
            job_remote = "f_WT=1"
        case "Remote":
            job_remote = "f_WT=2"
        case "Hybrid":
            job_remote = "f_WT=3"
    for index in range(1, len(remote_array)):
        match remote_array[index]:
            case "On-site":
                job_remote += "%2C1"
            case "Remote":
                job_remote += "%2C2"
            case "Hybrid":
                job_remote += "%2C3"

    return job_remote


def salary():
    salary = ""
    match config.salary[0]:
        case "$40,000+":
            salary = "f_SB2=1&"
        case "$60,000+":
            salary = "f_SB2=2&"
        case "$80,000+":
            salary = "f_SB2=3&"
        case "$100,000+":
            salary = "f_SB2=4&"
        case "$120,000+":
            salary = "f_SB2=5&"
        case "$140,000+":
            salary = "f_SB2=6&"
        case "$160,000+":
            salary = "f_SB2=7&"
        case "$180,000+":
            salary = "f_SB2=8&"
        case "$200,000+":
            salary = "f_SB2=9&"
    return salary


def sort_by():
    sort_by = ""
    match config.sort[0]:
        case "Recent":
            sort_by = "sortBy=DD"
        case "Relevant":
            sort_by = "sortBy=R"
    return sort_by


def date_posted():
    date_posted = ""
    match config.date_Posted[0]:
        case "Any Time":
            date_posted = ""
        case "Past Month":
            date_posted = "&f_TPR=r2592000&"
        case "Past Week":
            date_posted = "&f_TPR=r604800&"
        case "Past 24 hours":
            date_posted = "&f_TPR=r86400&"
    return date_posted


def generate_url_links():
    path = []
    for location in config.location:
        for keyword in config.keywords:
            url = CONSTANTS.linkJobUrl + "?f_AL=true&keywords=" + keyword + job_type() + remote() + check_job_location(
                location) + job_experience() + date_posted() + salary() + sort_by()
            path.append(url)
    return path
