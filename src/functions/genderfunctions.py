import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', endpoint_url='http://host.docker.internal:8000')
table = dynamodb.Table('ReferenceData')


class Gender:
    def __init__(self, item):
        if item is not None:
            self.ItemUUID = item.get('ItemUUID')
            self.ItemType = item.get('ItemType')
            self.Code = item.get('Code')
            self.Name = item.get('Name')
            if self.ItemType is None:
                self.ItemType = 'GENDER'
            self.Key = {'ItemUUID': self.ItemUUID, 'ItemType': self.ItemType}
        else:
            self.ItemType = 'GENDER'

    def create(self):
        if self.ItemUUID is None:
            self.ItemUUID = str(uuid.uuid4())
        return table.put_item(Item={'ItemUUID': self.ItemUUID, 'ItemType': self.ItemType,
                                    'Code': self.Code, 'Name': self.Name})

    def read(self):
        return table.get_item(Key=self.Key)

    def update(self):
        return table.update_item(Key=self.Key,
                                 UpdateExpression="set #c=:c, #n=:n",
                                 ExpressionAttributeValues={
                                     ':c': self.Code,
                                     ':n': self.Name
                                 },
                                 ExpressionAttributeNames={
                                     '#c': 'Code',
                                     '#n': 'Name'
                                 }
                                 )

    def delete(self):
        return table.delete_item(Key=self.Key)

    def getall(self):
        return table.query(
            IndexName='ItemTypes',
            KeyConditionExpression=Key('ItemType').eq(self.ItemType))


def gendercreate(event, context):
    dto = Gender(event['queryStringParameters'])
    ret_val = dto.create()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def genderupdate(event, context):
    dto = Gender(event['queryStringParameters'])
    ret_val = dto.update()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def genderget(event, context):
    uuid = event['queryStringParameters'].get('ItemUUID')
    response = table.get_item(Key={'ItemUUID': uuid, 'ItemType': 'GENDER'})
    print(response)


def genderread(event, context):
    item = event['queryStringParameters']
    dto = Gender(item)
    ret_val = dto.read()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def genderlistall(event, context):
    dto = Gender(None)
    ret_val = dto.getall()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def genderdelete(event, context):
    dto = Gender(event['queryStringParameters'])
    ret_val = dto.delete()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
