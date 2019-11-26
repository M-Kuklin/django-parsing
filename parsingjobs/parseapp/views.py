import requests
from bs4 import BeautifulSoup as bs
import time
import csv
from django.shortcuts import render

headers = {'accept': '*/*',
                     'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}

base_url_work_ua = 'https://www.work.ua/ru/jobs-python/?page=1'
base_url_hh = 'https://dnepr.hh.ua/search/vacancy?L_is_autosearch=false&area=5&clusters=true&currency_code=UAH&enable_snippets=true&text=python&page=0'


def work_ua_parse_lxml(base_url_work_ua,headers):
    jobs_work_ua = []
    urls = []
    urls.append(base_url_work_ua)
    session = requests.Session()
    request = session.get(base_url_work_ua,headers=headers)
    if request.status_code == 200:
        start = time.time()
        soup = bs(request.content,'lxml')
        try:
              paggination =  soup.find_all('ul',attrs={'class','pagination hidden-xs'})
              for links in paggination:
                     link = links.find_all('a')
                     count = int(link[-2].text)
                     for i in range(1,count+1):
                            url = f'https://www.work.ua/ru/jobs-python/?page={i}'
                            if url not in urls:
                                urls.append(url)
                                
        except:
            pass

    for url in urls:
        request = session.get(url,headers=headers)
        soup = bs(request.content,'lxml')
        divs = soup.find_all('div',attrs= {'class':'card card-hover card-visited wordwrap job-link' })
        for div in divs:
              try: 
                   title = div.find('a').text
                   href1 = div.find('a')['href']
                   href2 = 'https://www.work.ua'
                   href = href2+href1
                   corporation = div.find_all('div',attrs={'class':'add-top-xs'})
                   for corp in corporation:
                       try:
                        company = corp.find('b').text
                       except:
                           company = 'none'
                   content = div.find('p',attrs={'class':'overflow text-muted add-top-sm add-bottom'}).text
                   
                   jobs_work_ua.append({
                       'title':title,
                       'href':href,
                       'company':company,
                       'content':content.replace('\xa0',' ' ).replace('\n',' ')
                       })

              except:
                    pass
        print(len(jobs_work_ua))
    else:
        print('ERROR or Done ' + str(request.status_code))
    return jobs_work_ua    
           
            
def hh_parse_lxml (base_url_hh,headers):
    jobs_hh = []
    urls = []
    urls.append(base_url_hh)
    session = requests.Session()
    request = session.get(base_url_hh,headers=headers)
    if request.status_code == 200:
        start = time.time()
        soup = bs(request.content,'lxml')
        try:
            paggination = soup.find_all('a',attrs={'data-qa':'pager-page'})
            count = int(paggination[-1].text)
            for i in range(count):
                url = f'https://dnepr.hh.ua/search/vacancy?L_is_autosearch=false&area=5&clusters=true&currency_code=UAH&enable_snippets=true&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url,headers=headers)
        soup = bs(request.content,'lxml')
        divs = soup.find_all('div',attrs= {'data-qa':'vacancy-serp__vacancy' })
        for div in divs:
              try: 
                   title = div.find('a',attrs={'data-qa':'vacancy-serp__vacancy-title'}).text
                   href = div.find('a',attrs={'data-qa':'vacancy-serp__vacancy-title'})['href']
                   company = div.find('a',attrs={'data-qa':'vacancy-serp__vacancy-employer'}).text
                   text1 = div.find('div',attrs= {'data-qa':'vacancy-serp__vacancy_snippet_responsibility' }).text
                   text2 = div.find('div',attrs= {'data-qa':'vacancy-serp__vacancy_snippet_requirement' }).text
                   content = text1 + ' ' + text2
                   jobs_hh.append({
                    'title':title,
                    'href':href,
                    'company':company,
                    'content':content
                     })
              except:
                    pass
        print(len(jobs_hh))
    else:
        print('ERROR or Done ' + str(request.status_code))
    return jobs_hh
                
            

            

jobs_work_ua = work_ua_parse_lxml(base_url_work_ua,headers)
jobs_hh = hh_parse_lxml(base_url_hh,headers)

dir_jobs={}

key_title = 'title'
key_href = 'href'
key_company = 'company'
key_content = 'content'

#title
for i in range(0, len(jobs_work_ua)):
  dir_jobs.setdefault(key_title, [])
  dir_jobs[key_title].append( jobs_work_ua[i]['title'])
for i in range(0, len(jobs_hh)):
  dir_jobs.setdefault(key_title, [])
  dir_jobs[key_title].append( jobs_hh[i]['title'])
#href
for i in range(0, len(jobs_work_ua)):
  dir_jobs.setdefault(key_href, [])
  dir_jobs[key_href].append( jobs_work_ua[i]['href'])
for i in range(0, len(jobs_hh)):
  dir_jobs.setdefault(key_href, [])
  dir_jobs[key_href].append( jobs_hh[i]['href'])
#company
for i in range(0, len(jobs_work_ua)):
  dir_jobs.setdefault(key_company, [])
  dir_jobs[key_company].append( jobs_work_ua[i]['company'])
for i in range(0, len(jobs_hh)):
  dir_jobs.setdefault(key_company, [])
  dir_jobs[key_company].append( jobs_hh[i]['company'])
#content
for i in range(0, len(jobs_work_ua)):
  dir_jobs.setdefault(key_content, [])
  dir_jobs[key_content].append( jobs_work_ua[i]['content'])
for i in range(0, len(jobs_hh)):
  dir_jobs.setdefault(key_content, [])
  dir_jobs[key_content].append( jobs_hh[i]['content'])

  



   
    

#print(type(jobs))


#print (jobs_mass)

def index(request):
    
    data = { "job": dir_jobs}
    return render(request, "index.html", context=data)
    