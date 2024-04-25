# SEC EDGAR Filings Scraper

This project is designed to scrape SEC EDGAR filings for specified companies and analyze the text content of the filings.

## Setup

1. **Clone the repository:**

2. **Navigate to the project directory:**

3. **Create a virtual environment:**

    ```
    python3 -m venv env  
    ```

4. **Activate the virtual environment:**
- **On Windows:**
  ```
  env\Scripts\activate
  ```
- **On macOS and Linux:**
  ```
  source env/bin/activate
  ```

5. **Install dependencies:**

## Usage

1. **Fill the companies.txt file:**
- Open the `companies.txt` file located in the project directory.
- Add the ticker symbols of the companies you want to scrape, with each ticker symbol on a new line.

Example `companies.txt`:
```
AAPL
MSFT
NVDA
GOOGL
AMZN
META
TSM
JPM
WMT
TSLA
```



2. **Run the scraper:**

The current scraper uses the default start date of "1995-01-01" and end date of "2023-12-31" to download the 10-K filings.

The scraper will download SEC EDGAR filings for the companies listed in `companies.txt` and save them in the `data` directory.

Run the main program named `main.py`.

## Notes
- Make sure you have proper permissions to scrape data from the SEC EDGAR database.
- Be respectful of server limits and avoid overwhelming the SEC EDGAR servers with excessive requests.

3. Current Dataset Breakdown:
  AMZN Number of 10-K filings:  23
  AAPL Number of 10-K filings:  27
  WMT Number of 10-K filings:  29
  TSLA Number of 10-K filings:  13
  GOOGL Number of 10-K filings:  8
  MSFT Number of 10-K filings:  29
  META Number of 10-K filings:  11
  NVDA Number of 10-K filings:  22
  JPM Number of 10-K filings:  22