# import json
# import os
# import boto3
# import requests
# import base64

# def lambda_handler(event, context):
#     # Get subnet ID from the environment variables (provided by Terraform)
#     subnet_id = os.environ.get('PRIVATE_SUBNET_ID')  # Terraform will inject this value
    
#     # Replace these with your actual name and email (these can also be injected via environment variables)
#     full_name = "Sumit Dange" 
#     email = "sumitdange19@outlook.com"  
#     # API endpoint and security header
#     api_url = "https://bc1yy8dzsg.execute-api.eu-west-1.amazonaws.com/v1/data"
#     headers = {
#         'X-Siemens-Auth': 'test',
#         'Content-Type': 'application/json'
#     }
    
#     # Construct the payload dynamically
#     payload = {
#         "subnet_id": subnet_id,
#         "name": full_name,
#         "email": email
#     }
    
#     # Sending the POST request to the API endpoint
#     response = requests.post(api_url, headers=headers, json=payload)
    
#     # Log the response and return it
#     print("API Response: ", response.text)
    
#     # Handle and decode the Base64-encoded response (LogResult)
#     log_result_base64 = context.aws_request_id  # You can capture your log result if necessary
#     decoded_log_result = base64.b64decode(log_result_base64).decode('utf-8')
    
#     # Returning the decoded result as part of the response
#     return {
#         'statusCode': response.status_code,
#         'body': json.dumps({
#             'api_response': response.json(),
#             'decoded_log': decoded_log_result
#         })
#     }


import json
import os
import requests
import base64

def lambda_handler(event, context):
    # Get subnet ID from the environment variables (provided by Terraform)
    subnet_id = os.environ.get('PRIVATE_SUBNET_ID')  # Terraform will inject this value
    
    # Replace these with your actual name and email (these can also be injected via environment variables)
    full_name = os.environ.get('FULL_NAME', 'Sumit Dange')  # You can use environment variables for sensitive info
    email = os.environ.get('EMAIL', 'sumitdange19@outlook.com')
    
    # API endpoint and security header
    api_url = "https://bc1yy8dzsg.execute-api.eu-west-1.amazonaws.com/v1/data"
    headers = {
        'X-Siemens-Auth': 'test',
        'Content-Type': 'application/json'
    }
    
    # Construct the payload dynamically
    payload = {
        "subnet_id": subnet_id,
        "name": full_name,
        "email": email
    }
    
    try:
        # Sending the POST request to the API endpoint
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Log the response and return it
        print("API Response: ", response.text)
        
        # Capture the LogResult from event if it's provided (base64-encoded logs from Lambda invocation)
        log_result_base64 = event.get('LogResult')
        
        if log_result_base64:
            try:
                # Decode the base64 LogResult
                decoded_log_result = base64.b64decode(log_result_base64)
                
                # Try to decode as UTF-8 if the result is text-based
                try:
                    decoded_log_result = decoded_log_result.decode('utf-8')
                except UnicodeDecodeError:
                    # If it's not UTF-8 encoded, return it as binary data
                    decoded_log_result = base64.b64encode(decoded_log_result).decode('utf-8')
            except Exception as e:
                decoded_log_result = f"Error decoding LogResult: {str(e)}"
        else:
            decoded_log_result = "No LogResult found in the event."

        # Return the decoded result as part of the response
        return {
            'statusCode': response.status_code,
            'body': json.dumps({
                'api_response': response.json() if response.status_code == 200 else response.text,
                'decoded_log': decoded_log_result
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error invoking API or processing response', 'details': str(e)})
        }
