import requests
from urllib.parse import urlencode
from requests.structures import CaseInsensitiveDict

def habsang(text, name):
    url = f'https://{name}.gohakka.org'

    data = urlencode({
        'toivun': text,
        'socoi': 'tt1.wav',
    })
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    x = requests.post(url, headers=headers, data=data)
    return x.status_code

if __name__ == '__main__':
  r = habsang(
            'Kiung ha loiˇ liau dong senˊ qi',
            'tts-pin'
            )
  print(r)
headers = CaseInsensitiveDict({
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain"
})