import scrapy
from items import ShareItem
from scrapy_playwright.page import PageMethod  # Import PageMethod


class ProposedDividendsSpider(scrapy.Spider):
    name = "proposed_dividends"

    def start_requests(self):
        url = "https://www.sharesansar.com/proposed-dividend"
        yield scrapy.Request(
            url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[PageMethod("wait_for_selector", "#myTableLD")],
                errback=self.errback,
            ),
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        while True:
            for row in response.css("#myTableLD tbody tr"):
                name = row.css("td:nth-child(3) a::text").get()
                symbol = row.css("td:nth-child(2) a::text").get()
                bonus = row.css("td:nth-child(4)::text").get()
                cash = row.css("td:nth-child(5)::text").get()
                total = row.css("td:nth-child(6)::text").get()
                announcement_date = row.css("td:nth-child(7)::text").get()

                item = ShareItem()
                item["name"] = name.strip() if name else None
                item["symbol"] = symbol.strip() if symbol else None
                item["bonus"] = self.convert_to_float(bonus)
                item["cash"] = self.convert_to_float(cash)
                item["total"] = self.convert_to_float(total)
                item["announcement_date"] = (
                    announcement_date.strip() if announcement_date else None
                )

                yield item

            is_disabled = await page.evaluate(
                """() => {
                const disabledButton = document.querySelector('#myTableLD_next.disabled');
                return !!disabledButton;
            }"""
            )

            if is_disabled:
                break

            await page.click("#myTableLD_next")
            await page.wait_for_timeout(2000)  # Wait for 2 seconds

        await page.close()

    def convert_to_float(self, value):
        try:
            # Convert to float
            return float(value.replace(",", "").replace('"', ""))
        except (ValueError, AttributeError):
            # If conversion fails, return None
            return None

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
