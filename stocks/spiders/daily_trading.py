import scrapy
from stocks.items import StocksItem
import json


class DailyTrading(scrapy.Spider):
    name = "dailytradingdata"
    allowed_domains = ["sharesansar.com"]
    start_urls = ["https://www.sharesansar.com/live-trading"]

    def parse(self, response):
        result_data = []

        for row in response.css("#headFixed tbody tr"):
            data = [
                item.strip() for item in row.css("td::text").getall() if item.strip()
            ]
            symbol = row.css("td a::text").get()

            item = StocksItem()
            item["symbol"] = symbol
            item["ltp"] = data[1]

            item["open"] = data[-5]
            item["low"] = data[-3]
            item["previous_close"] = data[-1]

            result_data.append(item)

        # Save the scraped data to a JSON file
        with open(
            "/Users/subhesh/Workspace/share_sansar/stocks/stocks/data/daily_trading.json",
            "w",
        ) as f:
            json.dump([dict(item) for item in result_data], f)
