from requests_html import HTMLSession
from pprint import pprint
import json
drug_addresses = list()
session = HTMLSession()
headers = session.headers
headers['X-Requested-With'] = 'XMLHttpRequest'

url_state = 'https://www.tvoyaapteka.ru/bitrix/ajax/modal_geoip.php'
state_response = session.get(url_state)
states = state_response.html.xpath('//*[contains(@class, "regions")]/ul/li')

for info_state in states:
    state_id = info_state.xpath('//li/@data-id', first=True)
    state = info_state.xpath(f'//li[@data-id="{state_id}"]/text()', first=True)
    url_cities = f'https://www.tvoyaapteka.ru/bitrix/ajax/modal_geoip.php?action=get_towns&region_id={state_id}'
    cities_response = session.get(url_cities)
    cities = cities_response.json()
    for city_info in cities:
        home = 'https://www.tvoyaapteka.ru/'
        home_response = session.get(home)
        cookies = home_response.cookies
        city_id = city_info['ID']
        print(city_id)
        city = city_info['NAME']
        home_response.cookies.set('BITRIX_SM_S_CITY_ID', city_id, domain='.tvoyaapteka.ru', path='/')
        home_response = session.get(home, headers=headers, cookies=cookies)
        city_now = home_response.html.xpath('//*[@id="town_wrap"]/span/text()')
        print(city_now)
        url = 'https://www.tvoyaapteka.ru/bitrix/ajax/change_store_r.php'
        all_drugs = session.post(url, headers=headers, cookies=cookies)
        drug_info = all_drugs.html.xpath('//*[contains(@class, "apteka_item")]')
        for drug in drug_info:
            drug_dict = dict()
            drug_dict['address'] = drug.xpath('//*[@class="apteka_address"]/span/text()')
            drug_dict['latlon'] = [drug.xpath('//@data-lat', first=True), drug.xpath('//@data-lon', first=True)]
            drug_dict['name'] = drug.xpath('//*[@class="apteka_title"]/span/text()')
            drug_dict['workin_hours'] = [' '.join(list(map(str.strip,
                                                           drug.xpath('//*[@class="apteka_time"]/span/text()'))))]
            drug_addresses.append(drug_dict)

with open('tvoyaapteka.json', 'w') as write_file:
    json.dump(drug_addresses, write_file)

pprint(drug_addresses)
