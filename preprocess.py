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
        for script in soup(["script", "style", "head", "title", "meta"]):
            script.decompose()  # Rip it out

        return soup.get_text()
    
    def clear_non_informative_strings(self, text):
        patterns = [
            r'\b[a-zA-Z0-9]{20,60}\b',  # Basic long alphanumeric strings
            r'\bm[\d\w]{10,}\b',        # Patterns starting with 'm' followed by long alphanumeric characters
            r'\bg[\d\w]{7,}\.jpg\b',       # Specific pattern for graphics files
            r'(?<=\s)[a-zA-Z0-9]+\.htm(?=\s)',  # Matches 'htm' at the end of strings
            r'\b[a-z0-9]+\.gif\b',          # Matching 'gif' at the end of strings without a dot
            r'\b\d{1,2}px\b',           # CSS pixel settings
            r'style="[^"]*"',           # Inline CSS styles within quotes
            r'padding[^;"]*;?',         # CSS padding styles
            r'rowspan="\d+"',           # HTML rowspan attributes with quotes
            r'colspan="\d+"',           # HTML colspan attributes
            r'text-align:[^;"]*;?',     # CSS text-align properties
            r'font-family:[^;"]*;?',    # Font family styles
            r'font-size:[^;"]*;?',      # Font size specifications
            r'font-weight:[^;"]*;?',    # Font weight specifications
            r'line-height:[^;"]*;?',    # Line height specifications
            r'(?i)<div[^>]*>',          # Opening div tags with attributes, case-insensitive
            r'(?i)</div>',              # Closing div tags, case-insensitive
            r'(?i)<span[^>]*>',         # Opening span tags with attributes
            r'(?i)</span>',             # Closing span tags
            r'Arial',                   # Instances of Arial which might be left over from styles
            r'bottom',                  # CSS bottom properties
            r'background-color:[^;"]*;?',  # Background color CSS
            r'(?i)<table[^>]*>',        # Opening table tags with attributes
            r'(?i)</table>',            # Closing table tags
            r'(?i)<tr[^>]*>',           # Table row tags
            r'(?i)</tr>',               # Closing table row tags
            r'(?i)<td[^>]*>',           # Table data tags
            r'(?i)</td>',               # Closing table data tags
            
        ]
        for pattern in patterns:
            text = re.sub(pattern, ' ', text)
        return text        
    
    def preprocess_text(self, text):
        text = self.remove_html_tags(text)
        # Remove all script and style elements

        text = unidecode(text)  # Normalize Unicode characters
        text = text.lower()  # Convert to lowercase
        # Remove non-alphanumeric characters
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # text = re.sub(r'\d+', '', text)  # Remove numbers
        text = self.clear_non_informative_strings(text)
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)




if __name__ == "__main__":
    DATA_DIR = "data"
    CLEAN_DATA_DIR = "clean"
    company = "AAPL"


    preprocessor = Preprocessor()
    for company in os.listdir("data/sec-edgar-filings"):
        if company == ".DS_Store":
            continue
        print(company)
        SRC_DATA_PATH = f"{DATA_DIR}/sec-edgar-filings/{company}/10-K"
        DST_DATA_PATH = f"{CLEAN_DATA_DIR}/sec-edgar-filings/{company}/10-K"
        print(SRC_DATA_PATH)
        print(DST_DATA_PATH)
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


