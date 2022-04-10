from bs4 import BeautifulSoup
import random, json, os
import requests as rq

class Scraper():
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
        ]

    def GetSoup(self, url):
        res = rq.get(url, headers={"User-Agent": random.choice(self.user_agent_list)})
        soup = BeautifulSoup(res.text, "lxml")
        return soup

    def MakeTable(self, BankBuy, BankSell):
        CBK = set(list(BankBuy.keys())).intersection(set(list(BankSell.keys())))
        HTML = ""
        for key in sorted(list(CBK)):
            HTML += f'<tr class="footer-currency-table-body-row">\n<td id="{key}title" class="currency">{key}</td>\n<td id="{key}buy" class="buy">{BankSell[key]}</td>\n<td id="{key}sell" class="sell">{BankBuy[key]}</td>\n</tr>\n'
        return f'<tbody class="footer-currency-table-body">\n{HTML}</tbody>'


    def esunbank(self, _type="html"):
        BB = {}
        SB = {}
        soup = self.GetSoup(url="https://www.esunbank.com.tw/bank/personal/deposit/rate/forex/foreign-exchange-rates")
        for tr in soup.find_all("tr", class_="tableContent-light"):
            for data in tr.find_all("td"):
                if data.get("id"):
                    if data.get("id")[-4:] == "_BBR":
                        BB[data.get("id")[:-4]] = data.text.strip()
                    if data.get("id")[-4:] == "_SBR":
                        SB[data.get("id")[:-4]] = data.text.strip()
        if _type == "html":
            return self.MakeTable(BankBuy=BB, BankSell=SB), sorted(list(BB.keys()), key=lambda x:x)
        elif _type=="dict":
            return BB, SB

    def bot(self, _type="html"):
        BB = {}
        SB = {}
        soup = self.GetSoup(url="https://rate.bot.com.tw/xrt?Lang=zh-TW")
        for tr in soup.find_all("tr"):
            if tr:
                currency = tr.find("td", class_="currency")
                if currency:
                    name = currency.find("div", class_="visible-phone").text
                    name = name.strip().split("(")[1][:-1]
                    price = tr.find_all("td", class_="rate-content-sight")
                    Bbuy = price[0].text.strip()
                    Bsell = price[1].text.strip()
                    if "-" not in Bbuy and "-" not in Bsell:
                        BB[name] = Bbuy
                        SB[name] = Bsell
        if _type == "html":
            return self.MakeTable(BankBuy=BB, BankSell=SB), sorted(list(BB.keys()), key=lambda x:x)
        elif _type=="dict":
            return BB, SB

    def cathaybk(self, _type="html"):
        BB = {}
        SB = {}
        soup = self.GetSoup(url="https://www.cathaybk.com.tw/cathaybk/personal/deposit-exchange/rate/currency-billboard/")
        table = soup.find("table", class_="ratepc")
        for tr in table.find_all("tr", class_="rate_list"):
            td = tr.find_all("td", class_="td")
            name = td[0].text.strip().split("(")[1][:-1]
            if "-" not in td[1].text and "-" not in td[2].text:
                BB[name] = td[1].text.strip()
                SB[name] = td[2].text.strip()
        if _type == "html":
            return self.MakeTable(BankBuy=BB, BankSell=SB), sorted(list(BB.keys()), key=lambda x:x)
        elif _type=="dict":
            return BB, SB

    def citibank(self, _type="html"):
        BB = {}
        SB = {}
        soup = self.GetSoup(url="https://www.citibank.com.tw/TWGCB/APBAASDP/fxrts/flow.action?TTC=29&selectedBCC=TWD")
        table = soup.find("form", {"id":"flow"}).findChildren("table")[-2]
        for tr in table.find_all("tr")[2:]:
            td = tr.find_all("td")
            name = td[1].text.strip()
            BankSell = td[2].text.strip()
            BankBuy = td[3].text.strip()
            if "N/A" not in BankBuy+BankBuy:
                BB[name] = BankBuy
                SB[name] = BankSell
        if _type == "html":
            return self.MakeTable(BankBuy=BB, BankSell=SB), sorted(list(BB.keys()), key=lambda x:x)
        elif _type=="dict":
            return BB, SB

    def firstbank(self, _type="html"):
        BB = {}
        SB = {}
        soup = self.GetSoup(url="https://www.firstbank.com.tw/sites/fcb/ForExRatesInquiry")
        tbody = soup.find("table", class_="table").find("tbody")
        for tr in tbody.find_all("tr"):
            td = tr.find_all("td")
            if td[1].text.strip() == "即期":
                name = td[0].text.strip().split("(")[1][:-1]
                BB[name] = "".join(td[2].text.split())
                SB[name] = "".join(td[3].text.split())
        if _type == "html":
            return self.MakeTable(BankBuy=BB, BankSell=SB), sorted(list(BB.keys()), key=lambda x:x)
        elif _type=="dict":
            return BB, SB

    def scsb(self, _type="html"):
        BB = {}
        SB = {}
        soup = self.GetSoup(url="https://ibank.scsb.com.tw/netbank.portal?_nfpb=true&_pageLabel=page_other12&_nfls=false")
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
        if _type == "html":
            return self.MakeTable(BankBuy=BB, BankSell=SB), sorted(list(BB.keys()), key=lambda x:x)
        elif _type=="dict":
            return BB, SB


    def GetHistory(self, quote, currency):
        reference = {"6mon":"https://rate.bot.com.tw/xrt/quote/l6m/", "3mon":"https://rate.bot.com.tw/xrt/quote/ltm/", "1day":"https://rate.bot.com.tw/xrt/quote/day/"}
        url = reference.get(quote, False)
        if not url: return {"date":[], "BB":[], "BS":[]}

        dates = []
        BB = []
        BS = []

        soup = self.GetSoup(url=url+currency)
        table = soup.find("table").find("tbody")
        for tr in table.find_all("tr"):
            td = tr.find_all("td")

            date = td[0].text.strip()
            dates.append(date)

            BankBuy = td[4].text.strip()
            BB.append(float(BankBuy))

            BankSell = td[5].text.strip()
            BS.append(float(BankSell))
        return {"date":dates[::-1], "BB":BB[::-1], "BS":BS[::-1]}

    def Get_content_type_1_table(self, currencies):
        with open(os.path.join(os.path.dirname(__file__), "data", "history_data.json"), "r") as f:
            history_data = json.load(f)
        currency=rq.get('https://tw.rter.info/capi.php').json()
        picked = sorted(currencies, key=lambda key:float(currency[f"USD{key}"]["Exrate"]))
        HTML = ""
        for idx, key in enumerate(picked):
            currency_worth = "{:0<7}".format(str( 1 / currency[f"USD{key}"]["Exrate"] * currency["USDTWD"]["Exrate"] )[:7])

            Mon6_data = history_data[key]["Mon6"]
            Mon6_oldest = ((Mon6_data["BB"][-1]+Mon6_data["BS"][-1])/2)
            Mon6_newest = ((Mon6_data["BB"][0]+Mon6_data["BS"][0])/2)
            Mon6 = (Mon6_oldest - Mon6_newest)/Mon6_newest*100
            Mon6_text = "{:0<6}".format(str(abs(Mon6))[:6])
            Mon6_state = "green-arrow-up" if Mon6>0 else "red-arrow-down"

            Mon3_data = history_data[key]["Mon3"]
            Mon3_oldest = ((Mon3_data["BB"][-1]+Mon3_data["BS"][-1])/2)
            Mon3_newest = ((Mon3_data["BB"][0]+Mon3_data["BS"][0])/2)
            Mon3 = (Mon3_oldest - Mon3_newest)/Mon3_newest*100
            Mon3_text = "{:0<6}".format(str(abs(Mon3))[:6])
            Mon3_state = "green-arrow-up" if Mon3>0 else "red-arrow-down"

            # Day1_data = self.GetHistory("1day", key)
            Day1_data = history_data[key]["Day1"]
            Day1_oldest = ((Day1_data["BB"][-1]+Day1_data["BS"][-1])/2)
            Day1_newest = ((Day1_data["BB"][0]+Day1_data["BS"][0])/2)
            Day1 = (Day1_oldest - Day1_newest)/Day1_newest*100
            Day1_text = "{:0<6}".format(str(abs(Day1))[:6])
            Day1_state = "green-arrow-up" if Day1>0 else "red-arrow-down"

            HTML += "\n".join([
                f'<tr>',
                f'<td id="content-type1-table-idx" class="content-type1-table-idx">{idx+1}</td>',
                f'<td id="content-type1-table-name" class="content-type1-table-item">{key}</td>',
                f'<td id="content-type1-table-price" class="content-type1-table-item">{currency_worth}</td>',
                f'<td id="content-type1-table-6mon" class="content-type1-table-item"><span id="{Mon6_state}"></span>{Mon6_text}%</td>',
                f'<td id="content-type1-table-3mon" class="content-type1-table-item"><span id="{Mon3_state}"></span>{Mon3_text}%</td>',
                f'<td id="content-type1-table-1day" class="content-type1-table-item"><span id="{Day1_state}"></span>{Day1_text}%</td>',
                f'</tr>'
            ])
        return HTML

    def Get_content_type_3_chart(self):
        with open(os.path.join(os.path.dirname(__file__), "data", "now_data.json"), "r") as f:
            now_data = json.load(f)
        intersection = {}
        for bank, data in now_data.items():
            if not intersection:
                intersection = set(data["BB"].keys()).intersection(set(data["BS"].keys()))
            intersection = intersection.intersection(set(data["BB"].keys())).intersection(set(data["BS"].keys()))
        print(intersection)
        result = {}
        for bank in now_data.keys():
            result[bank] = {"BB":{}, "BS":{}}
            for key in intersection:
                result[bank]["BB"][key] = float(now_data[bank]["BB"][key])
                result[bank]["BS"][key] = float(now_data[bank]["BS"][key])
        return result


















