import json
from branch import Branch


def lambda_handler(event, context):
    item = json.loads(event.pop('body'))
    dto = Branch(item)
    ret_val = dto.delete()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
