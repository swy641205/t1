# -*- coding: utf-8 -*-

import re, time
import requests
from requests.structures import CaseInsensitiveDict

while 1:
    text = input("""=== 漢字翻譯羅馬字拼音 ===
> """)

    text_space= ""
    spaces= len(text)-1
    for word in text:
        text_space += word
        if spaces > 0:
            text_space += " "
            spaces-=1

    url = "https://fi-xii.gohakka.org/translate"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = '[{"src": "'+text_space+'", "id": 1}]'

    resp = requests.post(url, headers=headers, data=data.encode('utf-8'))

    result=resp.text
    print(result.encode('utf-8').decode('unicode-escape'))