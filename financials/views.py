from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scraper import Scraper  
import json
import time
from PIL import Image
import io 
import base64
import os
import sys
from django.conf import settings

sys.path.append('./financials')
import inferer
import cleaner

def index(request): 
    return render(request,"financials/home.html")

def insights(request): 
    return render(request,"financials/home.html")

def visualizations(request): 
    return render(request,"financials/home.html")

@csrf_exempt  
def loadData(request):
    if request.method == 'POST':
        # Extract parameters from the POST request
        data = json.loads(request.body)
        ticker = data.get('ticker')
        year = data.get('year') 

        os.chdir(settings.BASE_DIR)

        output_dir= os.path.join(settings.BASE_DIR,"test_workflow")

        # Initialize and run the scraper
        scraper = Scraper(ticker, f"{year}-01-01", f"{year}-12-31", output_dir=output_dir)
        response = scraper.data_scraper()
        print(response)

        time.sleep(2)

        target_folder = f"{output_dir}/sec-edgar-filings/{ticker}/10-K"
        visualizations_folder, results_file_path = processSavedResponse(target_folder)

        original_cwd = os.getcwd()  # Save the original working directory
        print("printing the current working directory: ",original_cwd)
        with open(results_file_path, 'r') as file:
            insights = file.read()

        # Collect images as base64 from the visualization folder
        images = []
        for image_name in os.listdir(visualizations_folder):
            image_path = os.path.join(visualizations_folder, image_name)
            with open(image_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                images.append(encoded_image)

        # Construct the JSON response with insights and images
        response_data = {
            'insights': insights,
            'images': images,
            'message': 'Data scraping and visualization completed successfully'
        }


        # Respond with success message (or more details if needed)
        return JsonResponse(response_data)

    # Return an error if not a POST request
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_latest_modified_folder(directory):
    # Get list of all items (files and folders) in the directory
    items = os.listdir(directory)
    
    # Filter out only the folders
    folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    
    # Sort the folders based on their modification times
    sorted_folders = sorted(folders, key=lambda folder: os.path.getmtime(os.path.join(directory, folder)), reverse=True)
    
    # Get the latest modified folder
    latest_folder = sorted_folders[0] if sorted_folders else None
    
    return latest_folder



def processSavedResponse(target_folder):
    folder = get_latest_modified_folder(target_folder)
    print("the saved folder is ",folder)
    file_path = f"{target_folder}/{folder}/full-submission.txt"

    print(file_path)

    sections = cleaner.clean_data(file_path=file_path)
    results, financial_table = inferer.infer_data(sections[:2])

    # Save the results in a text file
    results_file_path = f"{target_folder}/{folder}/results.txt"
    with open(results_file_path, "w") as file:
        for result in results:
            file.write(str(result) + "\n")

    # just generate visualizations for the last section
    code = inferer.generate_visualizations_code(results[-1], financial_table)
    # save the code in a python file
    code_file_path = f"{target_folder}/{folder}/viz_code.py"
    with open(code_file_path, "w") as file:
        file.write(code)

    

    visualizations_folder = f"{target_folder}/{folder}/visualizations"
    visualizations = inferer.run_visualizations_code(code, visualizations_folder)


    # Save the visualizations in the "visualizations" folder
    # for idx, visualization in enumerate(visualizations):
    #     image = Image.open(io.BytesIO(visualization))
    #     visualization_file = os.path.join(visualizations_folder, f"visualization_{idx}.png")
    #     image.save(visualization_file, format='PNG')

    print("Saved Visualizations to folder: ", visualizations_folder)

    return visualizations_folder, results_file_path


def send_image(request):
    pass
    



