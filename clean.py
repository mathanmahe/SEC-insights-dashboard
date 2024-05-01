import preprocess
import os

file_path = "data/sec-edgar-filings/AAPL/10-K/0000320193-17-000070/full-submission.txt"

with open(file_path, 'r') as file:
    text = file.read()
    

preprocessor = preprocess.Preprocessor()


preprocessed_text = preprocessor.preprocess_without_tokenize(text)

dst_file_path = "clean_data/sec-edgar-filings/AAPL/10-K/0000320193-17-000070/full-submission.txt"
os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)

with open(dst_file_path, 'w') as file:
    file.write(preprocessed_text)


