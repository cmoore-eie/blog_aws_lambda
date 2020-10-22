import json
from gender import Gender


def lambda_handler(event, context):
    dto = Gender(None)
    ret_val = dto.getall()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
