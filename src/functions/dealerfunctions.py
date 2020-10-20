import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', endpoint_url='http://host.docker.internal:8000')
table = dynamodb.Table('ReferenceData')
item_type = 'DEALER'


class Dealer:
    def __init__(self, item):
        if item is not None:
            try:
                self.Locations = item.pop('Locations')
            except:
                self.Locations = []
            self.ItemUUID = item.get('ItemUUID')
            self.Code = item.get('Code')
            self.Name = item.get('Name')
            self.EffectiveDate = item.get('EffectiveDate')
            self.ExpirationDate = item.get('ExpirationDate')
            self.Key = {'ItemUUID': self.ItemUUID, 'ItemType': item_type}

    def create(self):
        if self.ItemUUID is None:
            self.ItemUUID = str(uuid.uuid4())
        result = table.put_item(Item={'ItemUUID': self.ItemUUID, 'ItemType': item_type,
                                      'Code': self.Code, 'Name': self.Name,
                                      'EffectiveDate': self.EffectiveDate, 'ExpirationDate': self.ExpirationDate})
        for location in self.Locations:
            location_uuid = str(uuid.uuid4())
            table.put_item(Item={'ItemUUID': self.ItemUUID, 'ItemType': "DEALER_LOCATION#" + str(location_uuid),
                                 'Name': location.get('Name')})
        return result

    def read(self):
        return table.query(
            IndexName='item-uuid-index',
            KeyConditionExpression=Key('ItemUUID').eq(self.ItemUUID))

    def update(self):
        result = table.update_item(Key=self.Key,
                                   UpdateExpression="set #c=:c, #n=:n, #ef=:ef, #ex=:ex",
                                   ExpressionAttributeValues={
                                       ':c': self.Code,
                                       ':n': self.Name,
                                       ':ef': self.EffectiveDate,
                                       ':ex': self.ExpirationDate
                                   },
                                   ExpressionAttributeNames={
                                       '#c': 'Code',
                                       '#n': 'Name',
                                       '#ef': 'EffectiveDate',
                                       '#ex': 'ExpirationDate'
                                   }
                                   )
        for location in self.Locations:
            location_key = {'ItemUUID': self.ItemUUID, 'ItemType': location.get('ItemType')}
            table.update_item(Key=location_key,
                              UpdateExpression="set #n=:n, #a1=:a1, #a2=:a2",
                              ExpressionAttributeValues={
                                  ':n': location.get('Name'),
                                  ':a1': location.get('AddressLine1'),
                                  ':a2': location.get('AddressLine2')
                              },
                              ExpressionAttributeNames={
                                  '#n': 'Name',
                                  '#a1': 'AddressLine1',
                                  '#a2': 'AddressLine2'
                              }
                              )

        return 'Updates Complete'

    def delete(self):
        result = table.query(
            IndexName='item-uuid-index',
            KeyConditionExpression=Key('ItemUUID').eq(self.ItemUUID))
        items = result.pop('Items')
        for item in items:
            table.delete_item(Key={'ItemUUID': item.get('ItemUUID'), 'ItemType': item.get('ItemType')})
        return "Deletion Complete"

    def getall(self):
        return table.query(
            IndexName='item-type-index',
            KeyConditionExpression=Key('ItemType').eq(item_type))


def dealercreate(event, context):
    item = json.loads(event.pop('body'))
    dto = Dealer(item)
    ret_val = dto.create()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def dealerupdate(event, context):
    item = json.loads(event.pop('body'))
    dto = Dealer(item)
    ret_val = dto.update()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def dealerread(event, context):
    item = json.loads(event.pop('body'))
    dto = Dealer(item)
    ret_val = dto.read()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def dealerlistall(event, context):
    dto = Dealer(None)
    ret_val = dto.getall()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def dealerdelete(event, context):
    item = json.loads(event.pop('body'))
    dto = Dealer(item)
    ret_val = dto.delete()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
