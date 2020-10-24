import json
from ast import literal_eval

from branch import Branch


def lambda_handler(event, context):
    if 'queryStringParameters' in event:
        item = event.pop('queryStringParameters')
        if isinstance(item, str):
            item = literal_eval(item)
    else:
        item = event
    dto = Branch(item)
    ret_val = dto.read()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
