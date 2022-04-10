import requests as rq
from bs4 import BeautifulSoup
res = rq.get("https://www.cathaybk.com.tw/cathaybk/personal/deposit-exchange/rate/currency-billboard/")
with open("a.html", "w") as f:
    f.write(res.text)

BB = {}
SB = {}
soup = BeautifulSoup(res.text, "lxml")
table = soup.find("table", class_="ratepc")
for tr in table.find_all("tr", class_="rate_list"):
    td = tr.find_all("td", class_="td")
    name = "".join(td[0].text.split()).split("(")[1][:-1]
    if "-" not in td[1].text and "-" not in td[2].text:
        BB[name] = "".join(td[1].text.split())
        SB[name] = "".join(td[2].text.split())


print(BB)
print(SB)
CBK = set(list(BB.keys())).intersection(set(list(SB.keys())))
CS = """"""
for key in CBK:
    CS += f"""
<tr class="footer-currency-table-body-row">
    <td id="{key}title" class="currency">{key}</td>
    <td id="{key}buy" class="buy">{SB[key]}</td>
    <td id="{key}sell" class="sell">{BB[key]}</td>
</tr>
"""
print(CS)