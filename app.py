from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import re
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import textract
import subprocess
from io import BytesIO 

app = Flask(__name__)

def extract_info(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+\d{1,2}\s?)?(\d{3}[-\s]?\d{3}[-\s]?\d{4}|\(\d{3}\)\s?\d{3}[-\s]?\d{4})'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    return emails, phones


def extract_text_from_doc(file):
    # text = textract.process(doc).decode('utf-8')
        file_bytes = file.read()
        bytes_io = BytesIO(file_bytes)

        # Use antiword to extract text from the BytesIO object
        process = subprocess.Popen(['antiword', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        text, _ = process.communicate(input=bytes_io.read())
        text = text.decode('utf-8')
        
        return text


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        
        uploaded_files = request.files.getlist('file[]')
        cv_data = []

        for file in uploaded_files:

            filename = file.filename     

            if filename.endswith('.docx'):
                doc = Document(file)
                text = '\n'.join([para.text for para in doc.paragraphs])
        
            elif filename.endswith('.doc'):
                try:
                    text = extract_text_from_doc(file)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    continue
           
            elif filename.endswith('.pdf'):
                    pdf_reader =  PdfReader(file)
                    text = ''
                    for page_num in range(len(pdf_reader.pages)):
                        text += pdf_reader.pages[page_num].extract_text()
            else:
                continue
        
            emails, phones = extract_info(text)
            cv_data.append({'Filename': filename, 'Emails': emails, 'Phones': phones, 'Text': text})
    
            # Process each uploaded file and update 'data' dictionary
            # Example: extract_info(text) function to extract email IDs and phones from 'text'
            # Append extracted information to 'data' dictionary
        df = pd.DataFrame(cv_data)
        excel_file = 'output.xlsx'
        df.to_excel(excel_file, index=False)
        return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
