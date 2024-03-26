import json
import unicodedata
import re
from docx import Document

# Load the .docx file
document = Document('/content/UNEC1.docx')

document_data = {}
current_title = ""

# Function to clean up text
def clean_text(text):
    # Normalize text to replace non-ASCII characters with their closest ASCII equivalents
    normalized_text = unicodedata.normalize('NFKD', text)
    # Remove unwanted characters and sequences
    cleaned_text = ''.join(c for c in normalized_text if ord(c) < 128)
    # Add space or '-' between '90' and the following word
    cleaned_text = re.sub(r'(?<=90)([a-zA-Z])', r' \1', cleaned_text)
    # Remove extra spaces
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text.strip()

for paragraph in document.paragraphs:
    if paragraph.style.name.startswith("2023->1-TITLES"):
        current_title = clean_text(paragraph.text)
        document_data[current_title] = ""
    elif paragraph.style.name.startswith("2023->2-BODY"):
        cleaned_text = clean_text(paragraph.text)
        # Only add non-empty text to the value
        if cleaned_text:
            document_data[current_title] += cleaned_text + ' '

# Remove empty values
document_data = {k: v.strip() for k, v in document_data.items() if v.strip()}

# Convert the dictionary to JSON format
json_data = json.dumps(document_data, indent=4)
print(json_data)
