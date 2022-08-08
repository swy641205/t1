from http.client import HTTPConnection
from urllib.parse import urlencode
import json


def fanid(fa):
    tsuliau = dataraw(fa)

    lian = HTTPConnection('ai49.gohakka.org', port=80)
    header = {
        "Accept": "*/*",
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Origin': 'http://ai49.gohakka.org',
        'Referer': 'http://ai49.gohakka.org/',
    }
    lian.request("POST", "/py/translate.py", tsuliau, header)
    giedgo = lian.getresponse().read()
    huein = json.loads(giedgo)
    return huein['output']


def dataraw(fa):
    post_fa = fa.split('\n')
    print(post_fa)
    return urlencode({
        'page_name': 'hakkadic_rev',
        'input_lang': 'zh-tw',
        'input_txt': fa
    })


txt = '''一般人手頭繷斯較大慨，若係手頭緪斯較囓察。
飯毋罅食，連飯盆頭都分人食撇咧。
入到新環境愛定定適應。'''

if __name__ == '__main__':
    x = fanid(txt)
    print(x)
