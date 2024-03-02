from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.daily_trading import DailyTrading
from spiders.proposed_dividents import ProposedDividendsSpider


def run_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # Add the spiders to the process
    process.crawl(DailyTrading)
    process.crawl(ProposedDividendsSpider)

    # Start the process
    process.start()


if __name__ == "__main__":
    run_spiders()
