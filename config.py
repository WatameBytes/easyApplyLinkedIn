import os

browser = ["Chrome"]

# Linkedin credentials - if using PyCharm --> Edit Configs and find Environmental variables

email = os.environ['EMAIL']
password = os.environ['PASSWORD']

# get Chrome profile path by typing following url: chrome://version/
chromeProfilePath = r""

# Continent Locations: ["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
location = ["USA"]

# Keywords related to your job search
keywords = ["Java"]

# Job Experience: ["Internship", "Entry level" , "Associate" , "Mid-Senior level" , "Director" , "Executive"]
experience_Levels = ["Entry Level"]

# Job Posted: ["Any Time", "Past Month" , "Past Week" , "Past 24 hours"] - select only one
date_Posted = ["Past Month"]

# Job Type: ["Full-time", "Part-time" , "Contract" , "Temporary", "Volunteer", "Internship", "Other"]
job_Type = ["Full-time", "Part-time", "Contract"]

# ["On-site" , "Remote" , "Hybrid"]
remote = ["On-site", "Remote", "Hybrid"]

# Salary: ["$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", "$160,000+", "$180,000+",
# "$200,000+"]
salary = ["$80,000+"]

# Sort: ["Recent"] or ["Relevant"]
sort = ["Recent"]

# Blacklist Companies: ["Apple","Google"]
blacklist_Companies = []

# Blacklist Keywords In Title: ["manager", ".Net"]
blacklist_Titles = []
