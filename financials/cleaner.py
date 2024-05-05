
from bs4 import BeautifulSoup
import re

def clean_html_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    item_pattern = re.compile(r'Item\s\d{1,2}[A-Za-z]?\.')


    # Remove unwanted tags like <div>, <font>, and others
    for tag in soup.find_all(['div', 'font', 'span', 'a', 'p']):
        tag.unwrap()  # This replaces the tag with its contents

    #     # Check each <div> and unwrap it if it doesn't contain relevant item text
    # for div in soup.find_all('div'):
    #     if not re.search(item_pattern, div.get_text(strip=True)):
    #         div.unwrap()

    # Remove style, class, and other attributes from all tags except for table, tr, and td
    for tag in soup.find_all(True):
        if tag.name not in ['table', 'tr', 'td']:
            tag.attrs = {}  # Remove attributes
        else:
            # If you want to keep the table layout clean but simple:
            allowed_attrs = {'colspan', 'rowspan'}  # keep only these attributes
            for attr in list(tag.attrs):
                if attr not in allowed_attrs:
                    del tag[attr]

    # Optionally: Convert to plain text or handle the table as required
    return str(soup)

def clean_html_whitespace(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove white spaces around tags
    pretty_html = soup.prettify()
    cleaned_html = re.sub(r'>\s+<', '><', pretty_html)  # Remove spaces between tags

    # Remove multiple spaces within text
    def remove_multiple_spaces(text):
        return re.sub(r'\s+', ' ', text)

    # Apply the space removal for each text node
    for text in soup.find_all(text=True):
        cleaned_text = remove_multiple_spaces(text)
        text.replace_with(cleaned_text)

    return str(soup)

# Extracts the sections from a given 10-k containing all the tabular data
def find_section_tables(soup, start_text, end_text):
    tables = soup.find_all('table')
    start_index = None
    end_index = None
    count_start = 0
    count_end = 0

    # Iterate over each table to find the second occurrence of start_text
    for index, table in enumerate(tables):
        if table.find(lambda tag: tag.name == 'td' and start_text in tag.get_text()):
            count_start += 1
            if count_start == 2:
                start_index = index

        if table.find(lambda tag: tag.name == 'td' and end_text in tag.get_text()):
            count_end += 1
            if count_end == 2:
                end_index = index-1
                break  # Stop searching once the end index is found

    # If both start and end indices are found, extract all tables in that range
    if start_index is not None and end_index is not None and start_index < end_index:
        return tables[start_index:end_index + 1]  # Include the end_index table
    return None  # Return None if the section isn't found correctly

# Saves the section tables into an output file 
def save_section_tables(section_tables, output_file, heading):
    with open(output_file, 'w') as file:
        # Write the start of the HTML document
        file.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{heading}</title>\n</head>\n<body>\n")
        
        # Write each table's HTML content
        for table in section_tables:
            file.write(str(table))  # Write the HTML content of the table
            
        # Write the end of the HTML document
        file.write("</body>\n</html>")

def extract_sections(soup):
    # Extract tables between the second occurrences of "Item 5." and "Item 6." 
    # We use second occurences because the occurences always occur in the Table of Contents first, then the actual section.
    section5 = find_section_tables(soup, "Item 5.", "Item 6.")
    section6 = find_section_tables(soup, "Item 6.", "Item 7.")
    section7 = find_section_tables(soup, "Item 7.", "Item 8.")
    section8 = find_section_tables(soup, "Item 8.", "Item 9.")

    sections = [section5, section6, section7, section8]
    return sections

def is_relevant_div(tag):
    # Define a pattern that matches your specific criteria for div tags
    pattern = re.compile(r'Item\s\d{1,2}[A-Za-z]?\.')
    # Check if the text matches the item pattern
    return re.search(pattern, tag.get_text(strip=True)) is not None

# call this main function to extract tables, and get data in sections
def clean_data(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    soup = BeautifulSoup(text, 'html.parser')
    
    tables = soup.find_all('table') 
    # tables = []
    
    # for element in soup.find_all(['table', 'div']):  # Only iterate through table and div
    #     if element.name == 'table' or (element.name == 'div' and is_relevant_div(element)):
    #         tables.append(element)

    all_tables_html = ''.join([table.prettify() for table in tables])

    
    cleaned_html = clean_html_table(all_tables_html)
    cleaned_html = clean_html_whitespace(cleaned_html)

    soup = BeautifulSoup(cleaned_html, 'html.parser')

    sections = extract_sections(soup)

    return sections







