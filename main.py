import time

from linkedin import Linkedin
from utils import print_yellow

start_time = time.time()
Linkedin().linkedin_job_apply()
completed_time = time.time()
print_yellow("---Took: " + str(round((time.time() - start_time) / 60)) + " minute(s).")
