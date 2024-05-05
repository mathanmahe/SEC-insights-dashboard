from scraper import Scraper
import time
import os
import preprocess
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

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

def scrapeSingleFile():
    start_date = "2017-01-01"
    end_date = "2017-12-31"
    scraper = Scraper("AAPL", start_date, end_date, output_dir="./new_data")
    scraper.data_scraper()


def readTablesFromHtml():
    file_path = "data/sec-edgar-filings/AAPL/10-K/0000320193-17-000070/full-submission.txt"

    with open(file_path, 'r') as file:
        text = file.read()
        
    soup = BeautifulSoup(text, 'html.parser')

    # tables = pd.read_html(str(soup))

    # for i in tables:
    #     print(i)

    # Find all tables in the HTML content
    tables = soup.find_all('table')
    
    # List to hold all dataframes
    dataframes = []

    print(len(tables))

    output_file_path = "tables.html"

    all_tables_html = ''.join([table.prettify() for table in tables])

    # with open(output_file_path, 'w') as output_file:
    #     output_file.write(all_tables_html)
    
    # print(f"tables saved to {output_file_path}")


    soup = BeautifulSoup(all_tables_html, 'html.parser')
    first_idx, last_idx = find_section_bounds(soup, "Item 7.", "Item 9.")
    main_content = extract_section_html(soup, first_idx, last_idx)


    # main_content = extract_main_content_html(all_tables_html, "Item 1.", "Item 16.")

    output_file_path = "tables_extracted.html"
    with open(output_file_path, 'w') as output_file:
        output_file.write(main_content)
    
    print(f"tables_extracted saved to {output_file_path}")

# does not work well
def find_section_bounds(soup, first_item, last_item):
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table', 'div', 'span', 'a', 'font'])  # Adjust tag list as per your document's structure
    first_idx = last_idx = None
    for i, heading in enumerate(headings):
        if heading.string and first_item in heading.string.strip():
            first_idx = i
        if heading.string and last_item in heading.string.strip() and first_idx is not None:
            last_idx = i
            break

    return (first_idx, last_idx)

# does not work well
def extract_section_html(soup, first_idx, last_idx):
    if first_idx is not None and last_idx is not None:
        section_content = soup.contents[first_idx:last_idx]
        return ''.join(str(content) for content in section_content)
    return ""
    


def find_second_occurrences(soup, first_item, last_item):
    items = soup.find_all(text=True)
    # items = soup.find_all()
    first_idx = None
    last_idx = None
    first_count = 0
    last_count = 0

    print("items: ", type(items), len(items))

    for idx, item in enumerate(items):
        if first_item in item:
            first_count += 1
            if first_count == 2:
                first_idx = idx
        if last_item in item:
            last_count += 1
            if last_count == 2:
                last_idx = idx
                break

    return first_idx, last_idx


# extracts main content text
def extract_main_content(html_content, first_item, last_item):
    soup = BeautifulSoup(html_content, 'html.parser')
    first_idx, last_idx = find_second_occurrences(soup, first_item, last_item)
    
    if first_idx is not None and last_idx is not None:
        content_items = soup.find_all(text=True)[first_idx:last_idx]
        return ' '.join(content.strip() for content in content_items if content.strip())
    else:
        return "Relevant sections not found."

# extracts main content as html 
def extract_main_content_html(html_content, first_item, last_item):
    soup = BeautifulSoup(html_content, 'html.parser')
    first_idx, last_idx = find_second_occurrences(soup, first_item, last_item)
    
    if first_idx is not None and last_idx is not None:
        main_content = soup.find_all()[first_idx:last_idx]
        main_content_html = ''.join(content.prettify() for content in main_content)
        return main_content_html
    else:
        return None


def readSections():
    file_path = "data/sec-edgar-filings/AAPL/10-K/0000320193-17-000070/full-submission.txt"

    with open(file_path, 'r') as file:
        text = file.read()

    main_content = extract_main_content(text, "Item 1.", "Item 15.")
    
    output_file_path = "main_content.txt"

    with open(output_file_path, 'w') as output_file:
        output_file.write(main_content)
    
    print(f"Main content saved to {output_file_path}")

def main():
    # scrapeFiles()
    # printFolders()
    readTablesFromHtml()
    # scrapeSingleFile()

    # readSections()



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