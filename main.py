from scraper import Scraper
import time
import os
import preprocess
from bs4 import BeautifulSoup
import pandas as pd


def scrapeFiles():
    start_date = "1995-01-01"
    end_date = "2023-12-31"

    # Read company tickers from companies.txt
    with open("companies.txt", "r") as file:
        companies = [line.strip() for line in file]
                 
    for company in companies:
        scraper = Scraper(company, start_date, end_date)
        scraper.data_scraper()
        time.sleep(10)
        print("Sleeping 10s to obey server limits")


def main():
    # scrapeFiles()
    # printFolders()

    file_path = "data/sec-edgar-filings/AAPL/10-K/0000320193-17-000070/full-submission.txt"

    with open(file_path, 'r') as file:
        text = file.read()
        
    soup = BeautifulSoup(text, 'html.parser')
    tables = pd.read_html(str(soup))

    for i in tables:
        print(i)

def printFolders():
    print("original filings")
    path = "data/sec-edgar-filings/"
    print_from_path(path)

    print("\n cleaned filings")
    path = "clean/sec-edgar-filings/"
    print_from_path(path)

def print_from_path(path):
    for item in os.listdir(path):
        if item == ".DS_Store":
            continue
        count = 0
        for i in os.listdir(os.path.join(path, item, "10-K")):
            count+=1
        print(item, "Number of 10-K filings: ", count)

if __name__ == "__main__":
    main()