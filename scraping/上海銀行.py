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
res = rq.get(
    "https://ibank.scsb.com.tw/netbank.portal?_nfpb=true&_pageLabel=page_other12&_nfls=false",
    headers={"User-Agent": random.choice(user_agent_list)}
)
soup = BeautifulSoup(res.text, "lxml")
with open("a.html", "w") as f:
    f.write(res.text)



BB = {}
SB = {}
table = soup.find("table", class_="txt07")
for tr in table.find_all("tr")[3:]:
    td = tr.find_all("td")
    if td:
        name = td[1].find("span").text
        if "CASH" not in name:
            name = name.strip()
            if name not in BB.keys() and name not in SB.keys():
                BB[name] = td[2].find("span").text
                SB[name] = td[3].find("span").text


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