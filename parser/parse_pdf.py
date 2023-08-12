import os
import re
import fitz  # PyMuPDF
import json
from pdf_ocr.pdf_ocr import extract_and_ocr_pdf

# Path to the PDFs folder
pdfs_folder = "../pdfs"
output_json_file = "../dat.json"

# DEPRECATED
def search_pattern_in_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    extracted_values = []
    # pattern = r"εκμίσθωση αιγιαλού (.*?) .*?επιχείρησης (.*?) στ.*? (.*?), εμβαδού (.*?),.*?με.*?Διάρκεια μίσθωσης.*?μίσθωσης και λήγει την (.*?)[\.|σύμφωνα]"
    pattern = r"εκμίσθωση αιγιαλού (.*?) .*?επιχείρησης (.*?) στ.*? (.*?),.*?εμβαδού (.*?)τ\.μ\..*?Διάρκεια μίσθωσης.*?μίσθωσης και λήγει την (.*?)[\.|σύμφωνα]"

    text = ''
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
        # print(text)
    text = text.replace('\n', ' ')

    matches = re.findall(pattern, text, re.DOTALL)
    print(matches)
    for match in matches:
        value1, value2, value3, value4, value5 = [value.strip() for value in match]
        extracted_values.append((value2, value3, value1, value4, value5))
    
    pdf_document.close()
    return extracted_values

def main():
    pdf_files = [file for file in os.listdir(pdfs_folder) if file.endswith(".pdf")]
    all_extracted_values = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdfs_folder, pdf_file)
        print(pdf_file)
        extracted_values = extract_and_ocr_pdf(pdf_path)
        print(extracted_values)
        exit(1)
        
        if extracted_values:
            print(f"Pattern found in '{pdf_file}':")
            all_extracted_values.extend(extracted_values)
        else:
            print(f"No pattern found in '{pdf_file}'.")

    print("Writing to json")
    with open(output_json_file, 'w') as json_file:
        json.dump(all_extracted_values, json_file, indent=4)

    print("Results appended to 'output.json'")

if __name__ == "__main__":
    main()
