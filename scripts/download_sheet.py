import os
import io
import json
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define Google Drive API Scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    """Authenticates using the JSON key stored in environment variables."""
    key_json_str = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
    if not key_json_str:
        logging.error("GCP_SERVICE_ACCOUNT_KEY environment variable is not set.")
        raise ValueError("Missing GCP_SERVICE_ACCOUNT_KEY secret.")
    
    key_info = json.loads(key_json_str)
    credentials = Credentials.from_service_account_info(key_info, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

def download_file(file_id: str, output_filename: str):
    """Downloads an Excel file or exports a Google Sheet to XLSX format."""
    service = get_drive_service()
    
    # Check file metadata to see if it's a Google Sheet or an uploaded .xlsx
    file_metadata = service.files().get(fileId=file_id, fields='mimeType, name').execute()
    mime_type = file_metadata.get('mimeType')
    logging.info(f"Target File Found: {file_metadata.get('name')} (MIME: {mime_type})")

    if mime_type == 'application/vnd.google-apps.spreadsheet':
        # Export Google Sheets native format directly to XLSX
        request = service.files().export_media(
            fileId=file_id,
            mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        # Standard binary download for pre-existing .xlsx files stored on Drive
        request = service.files().get_media(fileId=file_id)

    fh = io.FileIO(output_filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            logging.info(f"Download Progress: {int(status.progress() * 100)}%")

    logging.info(f"Download complete! Saved to {output_filename}")

if __name__ == "__main__":
    # Target Google Drive File ID (replace default or pass via environment variable)
    TARGET_FILE_ID = os.getenv("DRIVE_FILE_ID", "YOUR_GOOGLE_DRIVE_FILE_ID_HERE")
    OUTPUT_FILE = "data_source.xlsx"
    
    download_file(TARGET_FILE_ID, OUTPUT_FILE)
