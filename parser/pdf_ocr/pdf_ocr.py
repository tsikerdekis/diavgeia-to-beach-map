import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import io
import os
import hashlib
from .extract_coordinates import extract_coordinates

pytesseract.pytesseract.tesseract_cmd = 'tesseract'

def preprocess_image(image):
    # Preprocess the image if needed (e.g., enhance, etc.)
    return image

def calculate_image_hash(image):
    # Calculate the hash of the image data
    image_hash = hashlib.md5(image.tobytes()).hexdigest()
    return image_hash

def upscale_image(image, upscale_factor):
    # Upscale the image by a given factor
    new_width = int(image.width * upscale_factor)
    new_height = int(image.height * upscale_factor)
    return image.resize((new_width, new_height), Image.LANCZOS)

def extract_and_ocr_pdf(pdf_path, output_dir="extracted_images", upscale_factor=10, extract_coord = False):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    extracted_coord = ""
    extracted_meta = ""

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Dictionary to store image hashes and corresponding text
    image_text_mapping = {}
    text = ''

    # Loop through all the pages
    for page_num in range(pdf_document.page_count):
        # Add page text somewhere
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")

        # Get the page
        page = pdf_document[page_num]

        if extract_coord:
            # Extract images from the page
            images = page.get_images(full=True)

            # Check if the page contains any images
            if images:
                # Loop through the extracted images
                for img_index, img in enumerate(images):
                    xref = img[0]

                    try:
                        # Get the image
                        img_obj = pdf_document.extract_image(xref)
                        img_data = img_obj["image"]
                        img_extension = img_obj["ext"].lower()

                        # Create a Pillow Image object from the image data
                        img_pil = Image.open(io.BytesIO(img_data))

                        # Check if the image is larger than 1000x2000
                        if img_pil.size[0] < 1500 and img_pil.size[1] < 1500:

                            # Calculate the hash of the image data
                            img_hash = calculate_image_hash(img_pil)

                            # Check if the image has already been processed
                            if img_hash not in image_text_mapping:
                                # Upscale the image
                                upscaled_img = upscale_image(img_pil, upscale_factor)

                                # Perform OCR on the upscaled image
                                img_text = pytesseract.image_to_string(upscaled_img, lang='eng')

                                # Store the image hash and corresponding text
                                image_text_mapping[img_hash] = img_text
                                
                                coord = extract_coordinates(img_text)

                                if (coord):
                                    # Append the OCR text to the extracted_text
                                    extracted_coord = coord
                    except Exception as e:
                        print(f"Error processing image {img_index + 1} on page {page_num + 1}: {e}")
                        continue

    # Close the PDF document
    pdf_document.close()

    # Cleanup text
    text = text.replace('\n', ' ')
    # print(text)

    # run pattern matching
    print("Running regular expression...")
    ")  της  επιχείρησης  ΘΑΛΑΣΣΙΑ  ΣΠΟΡ  στην  ΚΑΛΛΙΘΕΑ, εμβαδού 60,00τ.μ.,με συντεταγμένες: όπως αποτυπώνεται στους συνημμένους ορθοφωτοχάρτες ,  "
    pattern = r"\)\s*?της\s*?επιχείρησης\s*?(.*?)\s*?στ.+?\s+?(.*?),"
    matches = re.findall(pattern, text, re.DOTALL)
    # print(matches)
    for match in matches:
        value1, value2 = [value.strip() for value in match]
        extracted_meta = (value1, value2)
        break


    return extracted_meta, extracted_coord

if __name__ == "__main__":
    # Provide the path to your PDF file
    pdf_path = "../../pdfs/ΩΧΝ0ΩΕΘ-Λ95.pdf"
    result = extract_and_ocr_pdf(pdf_path)
    print(result)
