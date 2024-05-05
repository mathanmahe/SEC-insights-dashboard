import re
import time
from bs4 import BeautifulSoup
import os
import json
import google.generativeai as genai
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import base64


def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def clean_text(text):
    # Remove special characters and strip spaces
    text = str(text)
    text = re.sub(r'[^\w\s.,]', '', text)
    # Remove newlines and extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# extracts tables from html in to python list format
def extract_tables(soup):
    tables = soup.find_all('table')
    filtered_tables = [table for table in tables if len(table.find_all(['tr'])) >= 4 and len(table.find_all(['td'])) >= 5]
    print(f"length of tables {len(tables)} and filtered tables {len(filtered_tables)}")
    final_tables = []
    for idx,table in enumerate(filtered_tables):
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [clean_text(ele.text) for ele in cols if clean_text(ele.text)]
            if cols:  # This checks if cols is not empty after cleaning
                data.append(cols)
        print("Table", idx)
        print(data)
        final_tables.append(data)
    return final_tables

def initialize_model():
    # Example usage
    config_file = "config.json"
    config = read_config(config_file)

    # Access the Google API token
    GOOGLE_API_KEY = config.get("GOOGLE_API_TOKEN")

    genai.configure(api_key = GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    return model

# The main function that infers the data given a few sections
def infer_data(sections):

    model = initialize_model()
    
    results = []
    
    for section in sections:
        section_string = ''.join(str(t) for t in section)
        soup = BeautifulSoup(section_string, 'html.parser')
        final_tables = extract_tables(soup)
        print(f"there are {len(final_tables)} in this section")

        for table in final_tables:
            text = str(table) + "\nthese are the financial data from apple from a 10-K Filing. Summarize the data and provide insights from the table."    
        
            result = model.generate_content(text)
            print("waiting5s for each table")
            time.sleep(5)
            results.append(result)
    
    financial_table = final_tables[0]
    
    print("Done with inference")

    # Perform some extraction of from the models' response
    stripped_results = []
    for result in results:
        stripped_result = result.candidates[0].content.parts[0].text
        stripped_results.append(stripped_result)

    return stripped_results, financial_table

def generate_visualizations_code(result, financial_table):
    model = initialize_model()

    text = str(financial_table) + str(result) + "\nthese are the insights, for selected financial data over 5 years, give me python code to generate visualizations to represent these insights, saved using plt, and do not display visualizations using plt.show()"    

    result = model.generate_content(text)
    code = result.candidates[0].content.parts[0].text.replace("```", "")
    code = code.replace("python", "")
    return code

def run_visualizations_code(code, target_folder):
    # Ensure that the matplotlib figures are created in an Agg context

    original_cwd = os.getcwd()  # Save the original working directory
    os.makedirs(target_folder, exist_ok=True)  # Ensure target directory exists
    os.chdir(target_folder)  # Change to the target directory
    try:
        exec(code)
        images = []
        for i in plt.get_fignums():
            fig = plt.figure(i)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            images.append(image_base64)
            plt.close(fig)  # Close the figure after capturing it
        os.chdir(original_cwd)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        images = []
    
    print(f"there were a total of {len(images)} visualizations generated")
    return images