import os.path
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate


def scraping(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    rA = soup.find_all('span')

    Average_CPU_Mark = rA[24]

    CPU_Name = rA[26]

    record = [(str(CPU_Name.text), str(Average_CPU_Mark.text), url)]

    if os.path.exists("cpu.csv"):
        df = pd.read_csv("cpu.csv")
        t = df[df.CPU_Name == rA[26].text]
        if t.empty:
            t = pd.DataFrame(record)
            t.to_csv('cpu.csv', mode='a', index=False, header=False)

        n = df[(df.CPU_Name == rA[26].text) & (df.Average_CPU_Mark != int(rA[24].text))]
        if not n.empty:
            print("\nLe CPU Name existe deja mais avec un Average CPU Mark different.  Nouveau : " + rA[24].text)
            n = df[df.URL != url]
            n.to_csv('cpu.csv', index=False, encoding='utf-8')

            z = pd.DataFrame(record)
            z.to_csv('cpu.csv', mode='a', index=False, header=False)

        s = df[(df.CPU_Name == rA[26].text) & (df.Average_CPU_Mark == int(rA[24].text))]
        if not s.empty:
            print("\nLe CPU Name existe deja avec le meme Average CPU Mark")
    else:
        df = pd.DataFrame(record, columns=['CPU_Name', 'Average_CPU_Mark', 'URL'])
        df.to_csv('cpu.csv', index=False, encoding='utf-8')

    td = pd.read_csv('cpu.csv')

    print('\n')
    print(tabulate(td, headers='keys', tablefmt="simple"))
    print('\n')


'''
CALL FUNCTION
'''

'''
CPU_Name, Average_CPU_Mark, URL
Intel Core i5-8250U @ 1.60GHz, 7841, https://www.cpubenchmark.net/cpu.php?cpu=Intel+Core+i5-8250U+%40+1.60GHz
Intel Core i5-7400 @ 3.00GHz, 7391, https://www.cpubenchmark.net/cpu.php?cpu=Intel+Core+i5-7400+%40+3.00GHz&id=2929
Intel Core i3-4010U @ 1.70GHz, 2440, https://www.cpubenchmark.net/cpu.php?cpu=Intel+Core+i3-4010U+%40+1.70GHz&id=2012
Intel Core i7-7700HQ @ 2.80GHz,8866, https://www.cpubenchmark.net/cpu.php?cpu=Intel+Core+i7-7700HQ+%40+2.80GHz&id=2906
'''

htp = input("Entrez l'adresse URL? : ")

scraping(htp)