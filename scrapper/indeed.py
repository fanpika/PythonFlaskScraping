import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  # print(soup)
  pagination = soup.find("div", {"class":"pagination"})
  # print(pagination)

  pages = pagination.find_all("a")
  last_page = pages[-2].text.strip()
  return int(last_page)

def extract_job(html):
  # https://lets-hack.tech/programming/languages/python/bs4-text-or-string/
  title = html.find("h2", {"class":"title"}).find("a")["title"].strip()
  company = html.find("span", {"class":"company"}).text.strip().replace("\r", " ")
  location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"].strip()
  job_id = html["data-jk"].strip()

  return {
    "title":title, 
    "company":company, 
    "location":location, "link":f"https://www.indeed.com/viewjob?jk={job_id}"
    }

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    # print(f"&start={page*LIMIT}")
    print(f"Scraping Indeed: page: {page}")
    result = requests.get(f"{url}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    
    for result in results:
      jobs.append(extract_job(result))
  return jobs

def get_jobs(word):

  url = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"

  last_page = get_last_page(url)
  # print(last_page)
  return extract_jobs(1, url)
  # return extract_jobs(last_page, url)