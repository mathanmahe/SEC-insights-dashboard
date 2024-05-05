import requests
import re
import os

from sec_edgar_downloader import Downloader

class Scraper:
    def __init__(self, company_ticker, start_date, end_date, output_dir="./data"):
        # enter the class level variables that you would like to be used here
        self.company_ticker = company_ticker
        self.start_date = start_date
        self.end_date = end_date
        self.output_dir = output_dir

    def data_scraper(self):
        os.path.join(self.output_dir, self.company_ticker)
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        downloader = Downloader("Student", "mathanmahe99@gmail.com", self.output_dir)
        response = downloader.get("10-K", self.company_ticker, after=self.start_date, before=self.end_date, download_details=True)
        return response

        
