import json
from dealer import Dealer



def lambda_handler(event, context):
    if 'body' in event:
        item = json.loads(event.pop('body', event))
    else:
        item = event
    dto = Dealer(item)
    ret_val = dto.update()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
