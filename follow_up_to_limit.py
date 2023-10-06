import time
import requests

auto = 'Bearer'

header = {
    'accept': '*/*',
    'authorization': auto,
    'origin': 'https://warpcast.com',
    'referer': 'https://warpcast.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

for i in range(13000):
    js = {
        'targetFid': i
    }
    url = 'https://client.warpcast.com/v2/follows'
    res = requests.put(url=url, data=js, headers=header)
    print(res.text)
    time.sleep(0.1)