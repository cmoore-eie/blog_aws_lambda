import json
from branch import Branch


def lambda_handler(event, context):
    if 'queryStringParameters' in event:
        item = event.pop('queryStringParameters')
        if isinstance(item, str):
            item = literal_eval(item)
    else:
        item = event
    dto = Branch(item)
    ret_val = dto.delete()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
