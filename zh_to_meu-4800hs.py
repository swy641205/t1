# -*- coding: utf-8 -*-
import requests
import re
import json
import os
import time
from requests.structures import CaseInsensitiveDict
from urllib.parse import urlencode


def dialect_subdomain(dialect):
    if dialect == "MeuLid":
        name = 'xii'
        title = '四縣腔'
    if dialect == "SinZhug":
        name = 'hoi'
        title = '海陸腔'
    if dialect == "DungShe":
        name = 'tai'
        title = '大埔腔'
    if dialect == "SinZhu":
        name = 'pin'
        title = '四縣腔' # 饒平  意傳拼音壞了
    if dialect == "Lun":
        name = 'onn'
        title = '詔安腔'
    if dialect == "LiugDui":
        name = 'nxi'
        title = '四縣腔'
    return name, title


def fi_post(text, name):
    # 翻譯前，需將字之間加入空格
    text_with_space = " ".join(text)

    url = f"https://{name}.gohakka.org/translate"
    headers = CaseInsensitiveDict({
        "Content-Type": "application/json"
    })
    data = '[{"src":"%s","id":1}]' % text_with_space
    resp = requests.post(
        url,
        headers=headers,
        data=data.encode('utf-8')
    )
    return resp.text


def py_post(text, name):
    headers = CaseInsensitiveDict({
        "Content-Type": "application/json"
    })
    url = f'https://hts.ithuan.tw/'
    arg = f'標漢字音標?查詢腔口={name}&查詢語句={text}'

    resp = requests.get(url + arg)
    return resp.text


def translate(text, name):
    result = fi_post(text, name)
    # 移除 [[ ]]
    result = re.sub(r'^\[\[|\]\]$', '', result)
    # 客語字-移除文字空格
    if re.match('fi-', name):
        result = re.sub(' ', '', result)
    print('華轉客狀態: ', result)
    result_dict = json.loads(result)
    return result_dict['tgt']


# https://hts.ithuan.tw/標漢字音標?查詢腔口=詔安腔&查詢語句=早安
def pinyin(text, name):
    result = py_post(text, name)

    result_dict = json.loads(result)

    # 取得拼音
    results = ''.join(ls['臺灣客話'] for ls in result_dict['綜合標音'])
    # 去除標點符號
    pin_result = re.sub('[\u4e00-\u9fa5]', ' ', results)
    # 取得客字+拼音分詞
    pin_participle = result_dict['分詞']
    print('客轉拼:', pin_participle)
    print('客轉拼:', pin_result)
    return pin_result, pin_participle


def habsang(text, name):
    url = f'https://{name}.gohakka.org'

    data = urlencode({
        'toivun': text,
        'socoi': f'{dialect_get}.wav',
    })
    headers = CaseInsensitiveDict({
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    })
    x = requests.post(url, headers=headers, data=data)
    return x.status_code


# tts-hoi 海陸 SinZhug  缺5
# tts-nxi 南四縣 LiugDui
# tts-onn 詔安 Lun    V
# tts-pin 饒平 SinZhu  4訓練中
# tts-tai 大埔 DungShe 4還行吧/缺5
dialect_get = 'SinZhu'
repeat = 1
text = '整夜沒睡，工作一直打哈欠。'
for i in range(repeat):
    # text = input("""=== 漢字翻譯羅馬字拼音 ===\n> """)
    dialect, dialect_title = dialect_subdomain(dialect_get)
    fi_subdomain = f'fi-{dialect}'
    tts_subdomain = f'tts-{dialect}'
    zh_to_haka = translate(text, fi_subdomain)
    print('華轉客: ', zh_to_haka)
    haka_to_pin, *pin_participle = pinyin(zh_to_haka, dialect_title)
    hab = habsang(haka_to_pin, tts_subdomain)
    print('合聲狀態: ', hab)
