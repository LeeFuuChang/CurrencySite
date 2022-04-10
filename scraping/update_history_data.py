from Scraper import Scraper
import time, json, os
TheScraper = Scraper()
currencies = [
    "CAD",
    "JPY",#
    "USD",
    "AUD",
    "SGD",#
    "CNY",
    "EUR",
    "GBP",
    "HKD",
    "CHF",#
    "ZAR",#
    "SEK",#
    "NZD",#
    "THB",#
]
history_data = {}
for idx, key in enumerate(currencies):
    print("Scraping [His]:", "6mon", key)
    Mon6_data = TheScraper.GetHistory("6mon", key)
    print("Scraping [His]:", "3mon", key)
    Mon3_data = TheScraper.GetHistory("3mon", key)
    print("Scraping [His]:", "1day", key)
    Day1_data = TheScraper.GetHistory("1day", key)
    history_data[key] = {
        "Mon6":Mon6_data,
        "Mon3":Mon3_data,
        "Day1":Day1_data
    }
    time.sleep(1)
with open(os.path.join(os.path.dirname(__file__), "data", "history_data.json"), "w") as history_data_file:
    json.dump(history_data, history_data_file)


banks = {
    "esunbank", #玉山銀行
    "bot", #臺灣銀行
    "cathaybk", #國泰世華
    "citibank", #花旗銀行
    "firstbank", #第一銀行
    "scsb", #上海銀行
}
now_data = {}
for bank in banks:
    print("Scraping [Now]:", bank)
    BankBuy, BankSell = TheScraper.__getattribute__(bank)(_type="dict")
    now_data[bank] = {"BB":BankBuy, "BS":BankSell}
with open(os.path.join(os.path.dirname(__file__), "data", "now_data.json"), "w") as now_data_file:
    json.dump(now_data, now_data_file)
