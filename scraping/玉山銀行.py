import requests as rq
from bs4 import BeautifulSoup
res = rq.get("https://www.esunbank.com.tw/bank/personal/deposit/rate/forex/foreign-exchange-rates")

BB = {}
SB = {}
soup = BeautifulSoup(res.text, "lxml")
for tr in soup.find_all("tr", class_="tableContent-light"):
    for data in tr.find_all("td"):
        print(data.text)
        if data.get("id"):
            if data.get("id")[-4:] == "_BBR":
                BB[data.get("id")[:-4]] = data.text
            if data.get("id")[-4:] == "_SBR":
                SB[data.get("id")[:-4]] = data.text

print(BB)
print(SB)
CBK = set(list(BB.keys())).intersection(set(list(SB.keys())))
CS = """"""
for key in sorted(list(CBK)):
    CS += f"""
<tr class="footer-currency-table-body-row">
    <td id="{key}title" class="currency">{key}</td>
    <td id="{key}buy" class="buy">{SB[key]}</td>
    <td id="{key}sell" class="sell">{BB[key]}</td>
</tr>
"""
print(CS)