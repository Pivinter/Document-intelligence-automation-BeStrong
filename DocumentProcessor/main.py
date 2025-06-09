import os
import logging
import azure.functions as func
from azure.storage.fileshare import ShareFileClient
from azure.storage.blob import BlobClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Environment variables (setup in Azure Function App)
AZURE_FORM_RECOGNIZER_ENDPOINT = os.environ["FORM_RECOGNIZER_ENDPOINT"]
AZURE_FORM_RECOGNIZER_KEY = os.environ["FORM_RECOGNIZER_KEY"]
SHARE_URL = os.environ["AZURE_FILE_SHARE_FILE_URL"]
BLOB_CONN_STRING = os.environ["BLOB_STORAGE_CONN_STRING"]
BLOB_CONTAINER_NAME = os.environ["BLOB_CONTAINER_NAME"]

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Function triggered")

    try:
        # Connect to the File Share and download the file
        file_client = ShareFileClient.from_file_url(SHARE_URL)
        downloaded = file_client.download_file()
        pdf_bytes = downloaded.readall()

        # Send PDF to Form Recognizer
        doc_client = DocumentAnalysisClient(
            endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
            credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
        )

        poller = doc_client.begin_analyze_document(
            model_id="prebuilt-document",
            document=pdf_bytes,
            content_type="application/pdf"
        )
        result = poller.result()

        # Convert result to JSON string
        json_result = result.to_dict()

        # Upload JSON to Blob
        blob_name = "result.json"
        blob_client = BlobClient.from_connection_string(
            conn_str=BLOB_CONN_STRING,
            container_name=BLOB_CONTAINER_NAME,
            blob_name=blob_name
        )

        blob_client.upload_blob(str(json_result), overwrite=True)
        logging.info("JSON uploaded to Blob Storage.")

    except Exception as e:
        logging.error(f"Error: {e}")
