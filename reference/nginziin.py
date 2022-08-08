from argparse import ArgumentParser
import re
import csv
import io, os
from urllib.request import urlopen
from os import makedirs
from os.path import join
import pandas as pd

mai_lukdui = re.compile('（.+?）')


def main():
    miang = '/ngienbun-ngiliau'
    makedirs(miang, exist_ok=True)
    with open(join(miang, 'meu.txt'), 'wt') as meu_dong:
        with open(join(miang, 'fa.txt'), 'wt') as fa_dong:
            for hang in ngin():
                for meu, fa in zip(
                        hang['例句'].split('\n'), hang['翻譯'].split('\n')
                ):
                    meu = meu.strip()
                    fa = fa.strip()
                    if meu:
                        print(mai_lukdui.sub('', meu), file=meu_dong)
                        print(fa, file=fa_dong)


def ngin():
    github_bangtsi = ('https://raw.githubusercontent.com/'
                      'i3thuan5/Elearning-Hakka/main/csv_imtong/')
    jintsing_sului = [
        f'{github_bangtsi}{code}3-2.csv',
        f'{github_bangtsi}{code}3-1.csv',
        f'{github_bangtsi}{code}w.csv',
    ]
    for bangtsi in jintsing_sului:
        with urlopen(bangtsi) as tong:
            with io.StringIO(tong.read().decode('utf-8')) as tsuliau:
                text = csv.DictReader(tsuliau)
                yield from text


def other_dialect():
    miang = '/ngienbun-ngiliau'
    dialect_file = f'/dialect/{dialect}'
    read_file = pd.read_excel(f'{dialect_file}.xlsx')
    read_file.to_csv(f'{dialect_file}.csv', index=None, header=False)

    # add title to first line.
    with open(f'{dialect_file}.csv', 'r') as original:
        data = original.read()
    with open(f'{dialect_file}.csv', 'w') as modified:
        modified.write(",,例句,翻譯\n" + data)

    with open(join(miang, 'meu.txt'), 'at') as meu_dong:
        with open(join(miang, 'fa.txt'), 'at') as fa_dong:
            with open(f'{dialect_file}.csv', 'r') as op_csv:
                reader = csv.DictReader(op_csv)
                for hang in reader:
                    for meu, fa in zip(
                            hang['例句'].split('\n'), hang['翻譯'].split('\n')
                    ):
                        meu = meu.strip()
                        fa = fa.strip()
                        if meu:
                            print(mai_lukdui.sub('', meu), file=meu_dong)
                            print(fa, file=fa_dong)


if __name__ == '__main__':
    dialect = os.getenv('DIALECT')
    LANGS = ['SinZhug', 'DungShe', 'SinZhu', 'Lun', 'MeuLid']
    if dialect in LANGS:
        if dialect == 'SinZhug': code = 'ha'
        if dialect == 'DungShe': code = 'da'
        if dialect == 'SinZhu': code = 'rh'
        if dialect == 'Lun': code = 'zh'
        if dialect == 'MeuLid': code = 'si'
        main()
    other_dialect()
