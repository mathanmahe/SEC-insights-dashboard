# SEC EDGAR Filings Scraper

This project is designed to scrape SEC EDGAR filings for specified companies and analyze the text content of the filings.

I used a Django based backend for this, with JavaScript, HTML/CSS on the front end. 

It gets certain insights from certain sections in the SEC, currently Items 5,6,7,8 from the below typical structure of the 10-K but it can be expanded as needed.

Item 1. Business
Item 1A. Risk Factors
Item 1B. Unresolved Staff Comments
Item 2. Properties
Item 3. Legal Proceedings
Item 4. Mine Safety Disclosures
Item 5. Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities
Item 6. Selected Financial Data
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations
Item 7A. Quantitative and Qualitative Disclosures About Market Risk
Item 8. Financial Statements and Supplementary Data
Item 9. Changes in and Disagreements With Accountants on Accounting and Financial Disclosure
Item 9A. Controls and Procedures
Item 10. Directors and Executive Officers of the Registrant
Item 11. Executive Compensation
Item 12. Security Ownership of Certain Beneficial Owners and Management
Item 13. Certain Relationships and Related Transactions
Item 14. Principal Accountant Fees and Services
Item 15. Exhibits, Financial Statement Schedules
Item 16. Form 10-K Summary

It also needs to be more generalized, as each company files their SEC 10-k filings with a different kind of HTML format, and my code is not optimized to be generalized yet, which I can implement given more time. 

I chose insights from Item 5. and 6. because they talk about the stock market shares of the company, and selected financial data, which typically contains a lot of information about the financial data over 5 years, such as income, expenses, debt and liabilities, which are key insights someone might be looking for. 

a pdf of the generated insights can be found here: https://drive.google.com/file/d/1oCoShQC0yxqGz4HLypHVw2n25iSVXPwk/view?usp=sharing

a youtube link can be found here to demonstrate the webapp: https://youtu.be/v9LK9WO6VpI

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


Django APP
The backend contains a Django project named dashboardproject, with an app called financials.