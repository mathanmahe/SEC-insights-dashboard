import requests
import re
import os

from sec_edgar_downloader import Downloader

class Scraper:
    def __init__(self, company_ticker, start_date, end_date):
        # enter the class level variables that you would like to be used here
        self.company_ticker = company_ticker
        self.start_date = start_date
        self.end_date = end_date

    def data_scraper(self):
        output_dir = "./data"
        # os.path.join("./data", self.company_ticker)
        
        # # Create the output directory if it doesn't exist
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)

        downloader = Downloader("Student", "mathanmahe99@gmail.com", output_dir)
        downloader.get("10-K", self.company_ticker, after=self.start_date, before=self.end_date)

        
