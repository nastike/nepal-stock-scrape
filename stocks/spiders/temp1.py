import scrapy
from stocks.items import ShareItem
from playwright.async_api import async_playwright


class ProposedDividentsSpider(scrapy.Spider):
    name = "temp"

    async def start_requests(self):
        url = "https://www.sharesansar.com/proposed-dividend"
        yield scrapy.Request(url, meta={"playwright": True})

    async def parse(self, response):
        for row in response.css("#myTableLD tbody tr"):
            data = [item for item in row.css("td::text").getall()]
            symbol = row.css("td a::text").get()
            item = ShareItem()
            item["symbol"] = symbol
            item["bonus"] = data[1]
            item["cash"] = data[2]
            item["total"] = data[3]
            item["announcement_date"] = data[4]
            yield item

        # Check for pagination
        next_button_exists = True  # Implement your logic here

        if next_button_exists:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(response.url)  # Load the current page URL
                # Implement the logic to interact with the pagination mechanism using Playwright
                # This may involve clicking buttons, scrolling, or triggering JavaScript events
                # You may need to use page.click(), page.evaluate(), or similar functions

                # Wait for the page to update with new data if necessary
                # Then, extract data from the updated DOM using Scrapy's response object
                # You may need to use page.content() to get the updated HTML content

                # Close the browser
                await browser.close()
