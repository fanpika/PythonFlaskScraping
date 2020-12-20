from scrapper.indeed import get_jobs as get_indeed_jobs
from scrapper.stackoverflow import get_jobs as get_so_jobs

def scrape(word):
  indeed_jobs = get_indeed_jobs(word)
  # print(indeed_jobs)

  so_jobs = get_so_jobs(word)
  # print(so_jobs)

  jobs = indeed_jobs + so_jobs

  return jobs