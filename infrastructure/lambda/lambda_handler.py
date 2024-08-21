# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import json
import uuid
from ds_ticat.ModelManager import ModelManager

def lambda_handler(event, context):
    try:
        processed_event = json.loads(event['body'])
        review_id = str(uuid.uuid4())

        model_manager = ModelManager()
        if not model_manager.model:
            model_manager.validate_setup()
            model_manager.train()

        # Process valid events
        if processed_event and 'text' in processed_event:
            text = processed_event['text']

            # Invoke the model
            sentiment, confidence = model_manager.predict(text)

            response = {
                'statusCode': 200,
                'body': json.dumps({
                    'review_id': review_id,
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'text': text
                }),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
            }
        else:
            response = {
                'statusCode': 400,
                'body': json.dumps('Invalid input: No text provided for sentiment analysis'),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(f'Error processing request: {str(e)}'),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    return response
