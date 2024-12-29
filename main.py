from bs4 import BeautifulSoup
import lxml
import requests
import pandas as pd

job_list = []

for i in range(1,7):
    url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&luceneResultSize=2000&sequence={i}&searchTextSrc=ft&searchTextText=Python&txtKeywords=Python%2C&txtLocation='
    html_page = requests.get(url)

    soup = BeautifulSoup(html_page.content, 'lxml')

    all_jobs = soup.select('li.clearfix')
    for job in all_jobs:
        job_title = job.find('h2', class_='heading-trun')
        job_details_link = job_title.find('a')['href']
        job_title = job_title.find('a').text.strip()
        company_name = job.find('h3', class_='joblist-comp-name').text.strip()
        job_posted = job.find('span', class_="sim-posted").text.strip()
        clearfix = job.select("ul.top-jd-dtl.mt-16.clearfix li")
        locations = clearfix[0].text.strip()
        experience = clearfix[1].text.strip()
        salary = clearfix[2].text.strip()
        skills = []
        for skill in job.select('div.more-skills-sections span'):
            skills.append(skill.text.strip())

        skills = ', '.join(skills)
        job_list.append([company_name, job_title, job_posted, locations, experience, salary, skills, job_details_link])


heads = ["company", "job_title", "job_posted", "locations", "experience", "salary", "skills", "job_link"]
df = pd.DataFrame(job_list, columns=heads)

df.to_csv("jobs_list3.csv")
print("file saved..")