import json
from gender import Gender


def lambda_handler(event, context):
    item = json.loads(event.pop('body'))
    dto = Gender(item)
    ret_val = dto.update()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
