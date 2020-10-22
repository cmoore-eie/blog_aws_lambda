import json
from branch import Branch


def lambda_handler(event, context):
    dto = Branch(None)
    ret_val = dto.getall()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
