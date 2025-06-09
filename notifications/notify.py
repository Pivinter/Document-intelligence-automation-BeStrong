import os
import logging
import json
import requests
import azure.functions as func
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()

# Environment variables
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BLOB_CONTAINER_NAME = os.environ.get("BLOB_CONTAINER_NAME", "ocr-json-results")

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

def main(myblob: func.InputStream):
    logging.info(f"Blob trigger function processed blob: {myblob.name}")

    # Create a basic notification message
    message = f"New file uploaded to {BLOB_CONTAINER_NAME}/{myblob.name}\n"

    try:
        # Try to read and parse the JSON content
        json_content = myblob.read().decode('utf-8')
        json_data = json.loads(json_content)

        # Add additional details if JSON is valid
        
        message += "Document analysis completed successfully."
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON: {e}")
        message += "Failed to parse JSON content, but file was detected."

    # Send notifications regardless of JSON parsing
    send_discord_notification(message)
    send_telegram_notification(message)