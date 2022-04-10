import requests as rq
from bs4 import BeautifulSoup
import random
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
]
headers = {"User-Agent": random.choice(user_agent_list)}
res = rq.get("https://www.citibank.com.tw/TWGCB/APBAASDP/fxrts/flow.action?TTC=29&selectedBCC=TWD", headers=headers, timeout=200)
with open("a.html", "w") as f:
    f.write(res.text)

BB = {}
SB = {}
soup = BeautifulSoup(res.text, "lxml")

table = soup.find("form", {"id":"flow"}).findChildren("table")[-2]
for tr in table.find_all("tr")[2:]:
    td = tr.find_all("td")
    name = td[1].text.strip()
    BankSell = td[2].text.strip()
    BankBuy = td[3].text.strip()
    if "N/A" not in BankBuy+BankBuy:
        BB[name] = BankBuy
        SB[name] = BankSell

print(BB)
print(SB)
CBK = set(list(BB.keys())).intersection(set(list(SB.keys())))
CS = ""
for key in CBK:
    CS += f"""
<tr class="footer-currency-table-body-row">
    <td id="{key}title" class="currency">{key}</td>
    <td id="{key}buy" class="buy">{SB[key]}</td>
    <td id="{key}sell" class="sell">{BB[key]}</td>
</tr>
"""
print(CS)