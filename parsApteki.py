import requests
from json import JSONDecodeError

def response(url, *kwargs):
    """возвращает ответ сервера в jsonke"""
    data = []
    for i in kwargs:
        response = requests.get(url.format(i))
        if response.ok:
            try:
                datat = response.json()
            except JSONDecodeError:
                pass
            else:
                if datat:
                    data.append(datat)
    return data




if __name__=='__main__':

    url = 'https://www.tvoyaapteka.ru/bitrix/ajax/modal_geoip.php?action=get_towns&region_id={0}'
    dat = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}
    #установлено циклом от 1 до 1000
    id = [918, 919, 920, 921, 922, 923]

    d = response(url, id)

    print(d)