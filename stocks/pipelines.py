import os
import sqlite3
from scrapy.exceptions import NotConfigured
from itemadapter import ItemAdapter


class SQLitePipeline:
    def __init__(self, db_name):
        self.db_name = db_name

    @classmethod
    def from_crawler(cls, crawler):
        db_name = crawler.settings.get("DB_NAME", "scrapy_data.db")
        if not db_name:
            raise NotConfigured("DB_NAME setting is missing")
        return cls(db_name)

    def open_spider(self, spider):
        self.db_path = os.path.join(
            spider.settings.get("DATA_DIR", "data"), self.db_name
        )
        self.conn = sqlite3.connect(self.db_path)
        self.curr = self.conn.cursor()
        self.create_tables()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if spider.name == "dailytradingdata":
            self.store_daily_trading_data(adapter)
        elif spider.name == "proposed_dividends":
            self.store_proposed_dividends_data(adapter)
        return item

    def create_tables(self):
        # Create daily_trading_tb table if not exists
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_trading_tb (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                ltp REAL,
                open REAL,
                low REAL,
                previous_close REAL
            )
        """
        )

        # Create proposed_dividends_tb table if not exists
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS proposed_dividends_tb (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                name TEXT,
                bonus REAL,
                cash REAL,
                total REAL,
                announcement_date TEXT
            )
        """
        )

    def store_daily_trading_data(self, adapter):
        self.curr.execute(
            """
            INSERT INTO daily_trading_tb (symbol, ltp, open, low, previous_close)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                adapter["symbol"],
                adapter["ltp"],
                adapter["open"],
                adapter["low"],
                adapter["previous_close"],
            ),
        )

    def store_proposed_dividends_data(self, adapter):
        self.curr.execute(
            """
            INSERT INTO proposed_dividends_tb (symbol, name, bonus, cash, total, announcement_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                adapter["symbol"],
                adapter["name"],
                adapter["bonus"],
                adapter["cash"],
                adapter["total"],
                adapter["announcement_date"],
            ),
        )
