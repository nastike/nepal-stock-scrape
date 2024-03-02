# Nepal Stock Scrape

Nepal Stock Scrape is a web scraping project built with Scrapy to extract daily trading data and proposed dividends data from the Nepal Stock Exchange website ([www.sharesansar.com](https://www.sharesansar.com/)).

## Overview

This project consists of two spiders:
- **dailytradingdata**: Scrapes the daily trading data from the Nepal Stock Exchange.
- **proposed_dividends**: Scrapes the proposed dividends data from the Nepal Stock Exchange.

The extracted data is stored in a SQLite database.

## Installation

1. Clone this repository:
   git clone https://github.com/nastike/nepal-stock-scrape.git
   cd nepal-stock-scrape
2. Install the required dependencies:
    pip install -r requirements.txt
## Usage
To run the spiders and scrape data from the Share Sansar website, use the following commands:
1. FOr daily trading data:
    scrapy crawl dailytradingdata
2. For proposed dividends data:
    scrapy crawl proposed_dividends

