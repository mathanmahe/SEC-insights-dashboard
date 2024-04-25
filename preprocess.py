from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from unidecode import unidecode
import os

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

class Preprocessor:
    def __init__(self):
        nltk.download("stopwords")
        nltk.download("punkt")
        nltk.download("wordnet")
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def remove_html_tags(self, text) -> str:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    
    def preprocess_text(self, text):
        text = self.remove_html_tags(text)
        text = unidecode(text)  # Normalize Unicode characters
        text = text.lower()  # Convert to lowercase
        # Remove non-alphanumeric characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # text = re.sub(r'\d+', '', text)  # Remove numbers

        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)




if __name__ == "__main__":
    DATA_DIR = "data"
    CLEAN_DATA_DIR = "clean"
    company = "AAPL"
    SRC_DATA_PATH = f"{DATA_DIR}/sec-edgar-filings/{company}/10-K"
    DST_DATA_PATH = f"{CLEAN_DATA_DIR}/sec-edgar-filings/{company}/10-K"

    preprocessor = Preprocessor()

    for foldername in os.listdir(SRC_DATA_PATH):
        file_path = os.path.join(SRC_DATA_PATH, os.path.join(foldername, "full-submission.txt"))
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            preprocessed_text = preprocessor.preprocess_text(text)

            os.makedirs(os.path.join(DST_DATA_PATH, foldername), exist_ok=True)
            dst_file_path = os.path.join(DST_DATA_PATH, os.path.join(foldername, "full-submission.txt"))
            with open(dst_file_path, "w", encoding="utf-8") as dst_file:
                dst_file.write(preprocessed_text)
            
            print(f"Preprocessed text saved to: {dst_file_path}")

        break


