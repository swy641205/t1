import requests, csv
import pandas as pd
from http.client import HTTPConnection
from urllib.parse import urlencode
import json


def meu_dict():
    # 篩選腔調
    texts = set()
    # fieldnames={'id', '', '腔調', '內文'}
    reader = csv.DictReader(origin)
    for row in reader:
        if row['腔調'] == '四縣':
            texts.add(row['客語'])
    total = len(texts)
    print('共: %s 句' % total)

    # # 分段翻譯
    texts = tuple(texts)
    times = total # 1000  # total
    texts = texts[:times]
    num = 0
    nums = 0
    counts = 0
    limit = 10000 #5000
    chunk = ''
    result_list = []
    for i in range(times):
        txt = f'{texts[nums]}\n'
        count = len(txt)
        if counts + count >= limit:
            result = fanid(chunk).split('\n')
            result = [x for x in result if x]
            print(result)
            for i in result:
                result_list.append(i)
            # 字數統計&待翻譯字串
            counts = 0
            chunk = ''
        chunk += txt
        counts += count
        nums += 1

    # 存檔
    # 0 1 2    3
    # , , 客語, 華語
    lines = ''
    row_d_e = zip(texts, result_list)
    for d, e in row_d_e:
        print(f'{d}\n{e}\n\n')
        lines += f',,{d},{e}\n'
    save.write(lines)


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
    return urlencode({
        'page_name': 'hakkadic_rev',
        'input_lang': 'zh-tw',
        'input_txt': fa
    })


file = 'MeuLid_fa'
read_file = pd.read_excel(f'{file}.xlsx')
read_file.to_csv(f'{file}_tmp.csv', index=None, header=True)
with open(file + '_tmp.csv', 'r', encoding='utf-8') as origin, \
        open(file + '.csv', 'w', encoding='utf-8-sig') as save:
    meu_dict()
