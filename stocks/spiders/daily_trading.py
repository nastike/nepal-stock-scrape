# daily_trading_spider.py
import scrapy

from items import StocksItem


class DailyTrading(scrapy.Spider):
    name = "dailytradingdata"
    allowed_domains = ["sharesansar.com"]
    start_urls = ["https://www.sharesansar.com/live-trading"]

    def parse(self, response):
        result_data = []

        for row in response.css("#headFixed tbody tr"):
            data = [
                item.strip().replace('"', "").replace(",", "")
                for item in row.css("td::text").getall()
                if item.strip()
            ]
            symbol = row.css("td a::text").get()

            item = StocksItem()
            item["symbol"] = symbol
            item["ltp"] = data[1]
            item["open"] = data[-5]
            item["low"] = data[-3]
            item["previous_close"] = data[-1]

            result_data.append(item)

        yield from result_data
