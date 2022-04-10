import requests as rq
from bs4 import BeautifulSoup
res = rq.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")

BB = {}
SB = {}
soup = BeautifulSoup(res.text, "lxml")
for tr in soup.find_all("tr"):
    if tr:
        currency = tr.find("td", class_="currency")
        if currency:
            name = currency.find("div", class_="visible-phone").text
            name = "".join(name.split()).split("(")[1][:-1]
            price = tr.find_all("td", class_="rate-content-sight")
            Bbuy = "".join(price[0].text.split())
            Bsell = "".join(price[1].text.split())
            if "-" not in Bbuy and "-" not in Bsell:
                BB[name] = Bbuy
                SB[name] = Bsell

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
print(CBK)