import os
import logging
import json
import requests
import azure.functions as func
from azure.storage.fileshare import ShareFileClient
from azure.storage.blob import BlobClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()

# Environment variables
AZURE_FORM_RECOGNIZER_ENDPOINT = os.environ["FORM_RECOGNIZER_ENDPOINT"]
AZURE_FORM_RECOGNIZER_KEY = os.environ["FORM_RECOGNIZER_KEY"]
SHARE_URL = os.environ["AZURE_FILE_SHARE_FILE_URL"]
BLOB_CONN_STRING = os.environ["BLOB_STORAGE_CONN_STRING"]
BLOB_CONTAINER_NAME = os.environ["BLOB_CONTAINER_NAME"]
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_discord_notification(message: str):
    """Send a notification to Discord via Webhook."""
    if not DISCORD_WEBHOOK_URL:
        logging.error("DISCORD_WEBHOOK_URL not set")
        return
    try:
        payload = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logging.info("Discord notification sent successfully")
    except Exception as e:
        logging.error(f"Failed to send Discord notification: {e}")

def send_telegram_notification(message: str):
    """Send a notification to Telegram via Bot API."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logging.info("Telegram notification sent successfully")
    except Exception as e:
        logging.error(f"Failed to send Telegram notification: {e}")

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Function triggered")
    logging.info(f"Endpoint: {AZURE_FORM_RECOGNIZER_ENDPOINT}")
    logging.info(f"Key: {AZURE_FORM_RECOGNIZER_KEY[:4]}**** (masked for security)")
    logging.info(f"File URL: {SHARE_URL}")
    logging.info(f"Blob Container: {BLOB_CONTAINER_NAME}")

    try:
        # Connect to the File Share and download the file
        file_client = ShareFileClient.from_file_url(SHARE_URL)
        downloaded = file_client.download_file()
        pdf_bytes = downloaded.readall()
        logging.info("File downloaded successfully")

        # Send PDF to Form Recognizer
        doc_client = DocumentAnalysisClient(
            endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
            credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
        )

        poller = doc_client.begin_analyze_document(
            model_id="prebuilt-document",
            document=pdf_bytes
        )
        result = poller.result()
        logging.info("Document analysis completed")

        # Convert result to JSON string
        json_result = result.to_dict()
        logging.info(f"Form Recognizer result: {json.dumps(json_result, indent=2, ensure_ascii=False)}")

        # Upload JSON to Blob as valid JSON
        blob_name = "result.json"
        blob_client = BlobClient.from_connection_string(
            conn_str=BLOB_CONN_STRING,
            container_name=BLOB_CONTAINER_NAME,
            blob_name=blob_name
        )

        # Use json.dumps to ensure valid JSON
        blob_client.upload_blob(json.dumps(json_result, ensure_ascii=False), overwrite=True)
        logging.info("JSON uploaded to Blob Storage.")

        # Send notifications (optional, since BlobTrigger will also send them)
        message = f"New JSON file uploaded to {BLOB_CONTAINER_NAME}/{blob_name}\n"
        message += f"Pages detected: {len(json_result.get('analyzeResult', {}).get('pages', []))}\n"
        message += "Document analysis completed successfully."
        send_discord_notification(message)
        send_telegram_notification(message)

    except Exception as e:
        logging.error(f"Error: {e}")