import json
import boto3
import requests

def lambda_handler(event, context):
    url = "https://www.goody2.ai/send"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.5",
        "Content-Type": "text/plain",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0"
    }
    
    # Get the prompt from the event input
    prompt = event.get('prompt', None)
    if not prompt:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Prompt is required',
                'error': 'Prompt is required'
            })
        }
    
    body = {
        "message": prompt,
        "debugParams": None
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(body),
            stream=True,
            timeout=30
        )
        
        response.raise_for_status()
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data:"):
                    try:
                        data = json.loads(decoded_line[5:])
                        if "content" in data:
                            full_response += data["content"]
                    except json.JSONDecodeError:
                        pass
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Request successful',
                'response': full_response
            })
        }
    except requests.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Request failed',
                'error': str(e)
            })
        }
