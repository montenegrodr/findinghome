import re
import requests

proxy_list_src = 'http://spys.me/proxy.txt'
daft_url = 'http://www.daft.ie/'
ip_pattern = '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\:\d{2,5}'


def ls():
    r = requests.get(proxy_list_src)
    if r.status_code == 200:
        for ip in re.finditer(ip_pattern, r.text):
            yield ip.group(0)
    else:
        raise CouldNotFetchProxyList()


def findproxy():
    ips = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    for timeout in range(1, 20, 2):
        timeout = timeout/10.0
        for ip in ls():
            proxies = {
                'http': ip
            }
            try:
                r = requests.get(daft_url,
                                 headers=headers,
                                 proxies=proxies,
                                 timeout=timeout)
                if r.status_code == 200 and 'daft' in r.text:
                    ips.append({
                        'ip': ip,
                        'time': r.elapsed.microseconds
                    })
            except:
                pass
        if ips:
            ips = sorted(ips, key=lambda k: k['time'])
            break

    if not ips:
        raise CouldNotFindProxy

    return ips[0]['ip']


class CouldNotFetchProxyList(Exception):
    pass

class CouldNotFindProxy(Exception):
    pass