import os
import json
import time
import random
import requests
import re

# Path to the PDFs folder
pdfs_folder = "../pdfs"

# Load the JSON data
json_file = "../export.json"

def download_pdf(pdf_url, file_path):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(file_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"Downloaded: {pdf_url}")
        return True
    else:
        print(f"Failed to download: {pdf_url}")
        return False

def main():
    with open(json_file, "r") as f:
        data = json.load(f)

    if not os.path.exists(pdfs_folder):
        os.makedirs(pdfs_folder)

    total_records = len(data["decisionResultList"])
    downloaded_count = 0
    skipped_count = 0
    recalls = []

    for index, record in enumerate(data["decisionResultList"], start=1):
        if ("ΑΝΑΚΛΗΣΗ" in str(record)):
            match = re.search(r'ΥΠ\.ΑΡΙΘΜ\.ΑΔΑ (.+?)(?=",decisionTypeUid)', str(record))
            if match:
                recalls.append(match.group(1))
        if any(year in str(record) for year in ["2021", "2022", "2023"]) and "ΑΝΑΚΛΗΣΗ" not in str(record):
            pdf_url = record["documentUrl"]
            pdf_filename = pdf_url.split("/")[-1] + ".pdf"
            pdf_path = os.path.join(pdfs_folder, pdf_filename)

            if os.path.exists(pdf_path):
                print(f"[{index}/{total_records}] Skipping {pdf_url} (already exists)")
                skipped_count += 1
            else:
                if download_pdf(pdf_url, pdf_path):
                    downloaded_count += 1

                    # Add a random sleep between 5 and 10 seconds after a successful download
                    sleep_duration = random.randint(5, 10)
                    print(f"[{index}/{total_records}] Sleeping for {sleep_duration} seconds...")
                    time.sleep(sleep_duration)
        # Remove any recalls that may have been downloaded
        for recall in recalls:
            if os.path.exists(os.path.join(pdfs_folder, recall + ".pdf")):
                os.remove(os.path.join(pdfs_folder, recall + ".pdf"))

    print(f"Downloaded {downloaded_count} files.")
    print(f"Skipped {skipped_count} files.")
    print(f"Recalls removed {len(recalls)} files.")

if __name__ == "__main__":
    main()
