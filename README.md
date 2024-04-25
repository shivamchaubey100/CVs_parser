
# CV Information Extractor

This Flask application is designed to extract contact information (emails and phone numbers) from various types of CV files such as .docx, .doc, and .pdf. The extracted data is then compiled into an Excel file for easy analysis and management.

## Prerequisites

Make sure you have the following dependencies installed:

- Python 3.x
- Flask
- pandas
- python-docx
- PyPDF2

You can install these dependencies using pip:

```bash
pip install Flask pandas python-docx PyPDF2
```

Additionally, the application uses `antiword` to extract text from .doc files. Ensure that `antiword` is installed on your system.

## Usage

1. Clone or download this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Run the Flask application using the following command:

   ```bash
   python app.py
   ```

4. Open your web browser and go to [http://localhost:5000](http://localhost:5000) to access the application.

## Features

- **Upload CV Files**: You can upload one or multiple CV files in .docx, .doc, or .pdf format.
- **Extract Information**: The application extracts emails and phone numbers from the uploaded CV files.
- **Generate Excel File**: Extracted data is compiled into an Excel file (`output.xlsx`) and downloaded automatically.
- **Error Handling**: If there are any issues with processing a file, the application logs the error and continues with other files.

## Deployment

The application is currently deployed and live at [http://shivamchaubey100.pythonanywhere.com/](http://shivamchaubey100.pythonanywhere.com/).

## Disclaimer

This application is designed for demonstration purposes and may not handle all CV formats or edge cases. Use it responsibly and review the extracted data for accuracy.
