import scrapy
from stocks.items import ShareItem
from scrapy_playwright.page import PageMethod

# import json
import pandas as pd


class ProposedDividendsSpider(scrapy.Spider):
    name = "proposed_dividents"

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
        result_data = []

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
                item["bonus"] = bonus.strip() if bonus else None
                item["cash"] = cash.strip() if cash else None
                item["total"] = total.strip() if total else None
                item["announcement_date"] = (
                    announcement_date.strip() if announcement_date else None
                )

                result_data.append(item)

            is_disabled = await page.evaluate(
                """() => {
                const disabledButton = document.querySelector('#myTableLD_next.disabled');
                return !!disabledButton;
            }"""
            )

            if is_disabled:
                break

            await page.click("#myTableLD_next")
            # Wait for a js element / data here instead
            await page.wait_for_timeout(2000)  # Wait for 2 seconds

        await page.close()

        # Save the final result to a file
        df = pd.DataFrame(result_data)
        df.to_csv(
            "/Users/subhesh/Workspace/share_sansar/stocks/stocks/data/proposed_dividents.csv",
            index=False,
        )
        # with open(
        #     "/Users/subhesh/Workspace/share_sansar/stocks/stocks/data/proposed_dividents.json",
        #     "w",
        # ) as f:
        #     json.dump([dict(item) for item in result_data], f)

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
