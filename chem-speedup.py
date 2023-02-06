import pandas as pd

SPLITTER = '/'


"""
Данный инструмент предназначен для
сбора информации об ОВР потенциалах.

Для того, чтобы сохранить данные, нужно
ввести 'save'. Для просмотра всей таблицы
необходима команда 'show'. Если вдруг данные
в последней строке введены неверно, поможет
команда 'delete'.

Примеры:

элемент, нач. заряд, кон. заряд, потенциал

1) Au 1 0 2.5
   Au[+1] + e[-1] --> Au[0] (2.5V)

2) Br 0/2 -1 -0.5
   Br2[0] + 2e[-1] --> 2Br[-1]

"""


def norm(s):
    if int(s) > 0:
        return '+' + s
    return s


def comb(el, ch):
    if SPLITTER in ch:
        ch, index = ch.split(SPLITTER)
    else: index = ''
    return f'{el}{index}[{norm(ch)}]'


def construct_df(a, b, c):
    return pd.DataFrame({
        'from': a,
        'to': b,
        'potential (V)': c
    })


def save(df):
    df_srtd = df.sort_values(by=['from', 'to'])
    df_srtd.to_csv('result.csv', index=False)
    print('Saved!')


cb = input('Do you want to load existing csv? (y/n) ')

if cb.lower() == 'y':
    path = input('Path: ')
    df = pd.read_csv(path)
else:
    df = construct_df([], [], [])


while True:
    try:
        note = input('Input: ')

        if not note:
            save(df)
            break
        elif note == 'delete':
            df.drop(len(df) - 1, axis=0, inplace=True)
            print('Deleted last!')
            continue
        elif note == 'show':
            print(df)
            continue
        elif note == 'save':
            save(df)
            continue

        el, from_, to, potential = note.split()
        a, b = comb(el, from_), comb(el, to)

        if ((df['from'] == a) & (df['to'] == b)).any():
            print('This data exists.')
            continue
        
        to_append = construct_df([a], [b], [potential])
        to_append.set_index(pd.Index([len(df)]), inplace=True)
        df = pd.concat([df, to_append], axis=0)
    except Exception as ex:
        print('Try again:', ex)