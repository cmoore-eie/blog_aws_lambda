import json
from branch import Branch


def lambda_handler(event, context):
    if 'body' in event:
        item = json.loads(event.pop('body', event))
    else:
        item = event
    dto = Branch(item)
    ret_val = dto.read()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
