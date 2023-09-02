from linkedin_scraper import JobSearch, actions
import pandas as pd
import time

from selenium.webdriver.common.by import By

driver = webdriver.Chrome() //chromedriver.exe is saved in project folder itself
# if not, then give the path
# driver=webdriver.Chrome(path)

# login using id and passwrod...enter your id and password
email = "apurvamalani357@gmail.com"
password = "*******"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
# input("Press Enter")
job_search = JobSearch(driver=driver, close_on_complete=False, scrape=True)
job_listings = job_search.search("Software Developer") # returns the list of `Job` from the first page
driver.implicitly_wait(100000)

# url1='https://in.linkedin.com/jobs/software-developer-jobs?position=1&pageNum=0'
# driver=get(url1)
# driver.implicitly_wait(10)

# Get all links for these offers
links = []
# Navigate 13 pages
print('Links are being collected now.')
try:
    for page in range(2, 14):
        time.sleep(2)
        jobs_block = driver.find_element_by_class_name('jobs-search-results__list')
        jobs_list = jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')

        for job in jobs_list:
            all_links = job.find_elements_by_tag_name('a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute(
                        'href') not in links:
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # scroll down for each job element
            driver.execute_script("arguments[0].scrollIntoView();", job)

        print(f'Collecting the links in the page: {page - 1}')
        # go to next page:
        driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
        time.sleep(3)
except:
    pass
print('Found ' + str(len(links)) + ' links for job offers')

# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = []
job_desc = []

i = 0
j = 1

# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i in range(len(links)):
    try:
        driver.get(links[i])
        i = i + 1
        time.sleep(2)
        # Click See more.
        driver.find_element_by_class_name("artdeco-card__actions").click()
        time.sleep(2)
    except:
        pass

    # Find the general information of the job offers
    contents = driver.find_elements_by_class_name('p5')
    for content in contents:
        try:
            job_titles.append(content.find_element_by_tag_name("h1").text)
            company_names.append(content.find_element_by_class_name("jobs-unified-top-card__company-name").text)
            company_locations.append(content.find_element_by_class_name("jobs-unified-top-card__bullet").text)
            work_methods.append(content.find_element_by_class_name("jobs-unified-top-card__workplace-type").text)
            post_dates.append(content.find_element_by_class_name("jobs-unified-top-card__posted-date").text)
            work_times.append(content.find_element_by_class_name("jobs-unified-top-card__job-insight").text)
            print(f'Scraping the Job Offer {j} DONE.')
            j += 1
        except:
            pass
        time.sleep(2)

        # Scraping the job description
    job_description = driver.find_elements_by_class_name('jobs-description__content')
    for description in job_description:
        job_text = description.find_element_by_class_name("jobs-box__html-content").text
        job_desc.append(job_text)
        print(f'Scraping the Job Offer {j}')
        time.sleep(2)

    # Creating the dataframe
df = pd.DataFrame(list(zip(job_titles, company_names,
                           company_locations, work_methods,
                           post_dates, work_times)),
                  columns=['job_title', 'company_name',
                           'company_location', 'work_method',
                           'post_date', 'work_time'])

# Storing the data to csv file
df.to_csv('job_offers.csv', index=False)

# Output job descriptions to txt file
with open('job_descriptions.txt', 'w', encoding="utf-8") as f:
    for line in job_desc:
        f.write(line)
        f.write('\n')
