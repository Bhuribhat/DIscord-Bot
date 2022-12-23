from bs4 import BeautifulSoup
import pandas as pd
import requests


def find_jobs(keyword, unwanted_skill):
    location = "Thailand"
    DOMAIN = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch"
    FILTER = f"&from=submit&txtKeywords={keyword}&txtLocation={location}"

    html = requests.get(DOMAIN + FILTER).text
    soup = BeautifulSoup(html, "html.parser")
    work = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    jobs = {
		'Company Name': [], 
		'Skills Required': [],
		'Job Description': [],
		'More Information': []
    }
    for candidate in work:
        published_date = candidate.find('span', class_ = 'sim-posted').span.text

        if 'few' in published_date:
            company_name  = candidate.find('h3', class_ = 'joblist-comp-name').text.replace(' ', '')
            descriptions  = candidate.find('ul', class_ = 'list-job-dtl clearfix').li.text.replace('  ', ' ')
            descriptions  = descriptions.split('...')[0].split(':')[1].replace('Overview', '')
            skill_require = candidate.find('span', class_ = 'srp-skills').text.replace('  ', ' ')
            more_detailed = candidate.header.h2.a['href']

            if unwanted_skill in skill_require: continue
            jobs['Company Name']    += [company_name.strip()]
            jobs['Skills Required'] += [skill_require.strip()]
            jobs['Job Description'] += [descriptions.strip()]
            jobs['More Information'] += [more_detailed.strip()]

    # save to csv file
    DF = pd.DataFrame(jobs)
    DF.to_csv(".\\assets\\jobs.csv", encoding='utf-8')
    return DF