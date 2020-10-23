import json
from gender import Gender


def lambda_handler(event, context):
    if 'body' in event:
        item = json.loads(event.pop('body', event))
    else:
        item = event
    dto = Gender(item)
    ret_val = dto.delete()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
