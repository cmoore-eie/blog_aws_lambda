import json
from gender import Gender


def lambda_handler(event, context):
    if 'queryStringParameters' in event:
        item = event.pop('queryStringParameters')
        if isinstance(item, str):
            item = literal_eval(item)
    else:
        item = event
    dto = Gender(item)
    return_item = dto.read()

    response = {
        'statusCode': 200,
        "body": json.dumps(return_item),
    }
    return response
