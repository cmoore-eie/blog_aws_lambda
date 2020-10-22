import json
from dealer import Dealer


def lambda_handler(event, context):
    dto = Dealer(None)
    ret_val = dto.getall()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
