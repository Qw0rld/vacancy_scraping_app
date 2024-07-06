from bs4 import BeautifulSoup
import requests

items = 100

headers = {
  'Host': 'hh.ru',
  'User-Agent': 'Safari',
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

def extract_max_page(url):
  hh_reqs = requests.get(url, headers=headers)
  hh_bs = BeautifulSoup(hh_reqs.text, 'html.parser')

  pr = hh_bs.find_all("span", {'class': 'pager-item-not-in-short-range'})

  pages = []

  for page in pr:
    pages.append(int(page.find('a').text))

  return  pages[-1]


def extract_vac(html):
  vac_data = {'title': '', 'com_name': '', 'city_salary': '', 'exp': ''}
  title_elem = html.find('a')
  if title_elem:
    vac_data['title'] = title_elem.text

  com_name_elem = html.find('span', {'class': 'company-info-text--vgvZouLtf8jwBmaD1xgp'})
  if com_name_elem:
    vac_data['com_name'] = com_name_elem.text.strip()

  city_salary_elem = html.find('span', {'class': 'fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni'})
  if city_salary_elem:
    vac_data['city_salary'] = city_salary_elem.text

  exp_elem = html.find('span', {'class': 'label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM'})
  if exp_elem:
    vac_data['exp'] = exp_elem.text

  return vac_data

def extract_hh_vacs(last_page, url):
  vacs = []
  for page in range(last_page):
    print(f'HeadHunter: парсинг страницы {page}')
    result = requests.get(f'{url}&page={page}', headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class': 'vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter'})

    for result in results:
      vac = extract_vac(result)
      vacs.append(vac)
  return vacs

def get_vacs(keyword):
  url = f'https://hh.ru/search/vacancy?items_on_page={items}&text={keyword}'
  max_page = extract_max_page(url)
  vacs = extract_hh_vacs(max_page, url)
  return vacs