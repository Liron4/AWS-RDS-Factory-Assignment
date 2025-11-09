import json
import logging
from logic import process_request

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received {len(event['Records'])} records from SQS")
    
    for record in event['Records']:
        try:
            sns_message = json.loads(record['body'])
            request_data = json.loads(sns_message['Message'])
            
            logger.info(f"Processing request for: {request_data.get('db_name')}")
            
            pr_url = process_request(request_data)
            
            logger.info(f"Successfully created PR: {pr_url}")

        except Exception as e:
            logger.error(f"Failed to process request: {e}")
            raise e

    return {"status": "success"}
