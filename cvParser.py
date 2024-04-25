import os
import re
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import textract 

# Function to extract email IDs and contact numbers from text
def extract_info(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+\d{1,2}\s?)?(\d{3}[-\s]?\d{3}[-\s]?\d{4}|\(\d{3}\)\s?\d{3}[-\s]?\d{4})'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    return emails, phones

# Function to process CV files and extract information

def extract_text_from_doc(doc_path):
    text = textract.process(doc_path).decode('utf-8')
    return text


def process_cv_files(cv_dir):
    cv_data = []
    
    for filename in os.listdir(cv_dir):
        if filename.endswith('.docx'):
            doc = Document(os.path.join(cv_dir, filename))
            text = '\n'.join([para.text for para in doc.paragraphs])
        
        elif filename.endswith('.doc'):
            try:
                text = extract_text_from_doc(os.path.join(cv_dir, filename))
            except:
                continue
           
        elif filename.endswith('.pdf'):
            with open(os.path.join(cv_dir, filename), 'rb') as file:
                pdf_reader =  PdfReader(file)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
        else:
            continue
        
        emails, phones = extract_info(text)
        cv_data.append({'Filename': filename, 'Emails': emails, 'Phones': phones, 'Text': text})
    
    return pd.DataFrame(cv_data)


cv_directory = 'sample2'
cv_dataframe = process_cv_files(cv_directory)
output_file = 'Excels/output.xlsx'
cv_dataframe.to_excel(output_file, index=False)
