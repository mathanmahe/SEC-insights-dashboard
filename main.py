from scraper import Scraper
import time
import os

def main():
    start_date = "1995-01-01"
    end_date = "2023-12-31"

    # # Read company tickers from companies.txt
    # with open("companies.txt", "r") as file:
    #     companies = [line.strip() for line in file]
                 
    # for company in companies:
    #     scraper = Scraper(company, start_date, end_date)
    #     scraper.data_scraper()
    #     time.sleep(10)
    #     print("Sleeping 10s to obey server limits")

    path = "data/sec-edgar-filings/"
    for item in os.listdir(path):
        count = 0
        for i in os.listdir(os.path.join(path, item, "10-K")):
            count+=1
        print(item, "Number of 10-K filings: ", count)

if __name__ == "__main__":
    main()