import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', endpoint_url='http://host.docker.internal:8000')
table = dynamodb.Table('ReferenceData')


class Branch:
    def __init__(self, item):
        if item is not None:
            self.ItemUUID = item.get('ItemUUID')
            self.ItemType = item.get('ItemType')
            self.Code = item.get('Code')
            self.Name = item.get('Name')
            self.BranchType = item.get('BranchType')
            self.EffectiveDate = item.get('EffectiveDate')
            self.ExpirationDate = item.get('ExpirationDate')
            if self.ItemType is None:
                self.ItemType = 'BRANCH'
            self.Key = {'ItemUUID': self.ItemUUID, 'ItemType': self.ItemType}
        else:
            self.ItemType = 'BRANCH'

    def create(self):
        if self.ItemUUID is None:
            self.ItemUUID = str(uuid.uuid4())
        return table.put_item(Item={'ItemUUID': self.ItemUUID, 'ItemType': self.ItemType,
                                    'Code': self.Code, 'Name': self.Name,
                                    'EffectiveDate': self.EffectiveDate, 'ExpirationDate': self.ExpirationDate})

    def read(self):
        return table.get_item(Key=self.Key)

    def update(self):
        return table.update_item(Key=self.Key,
                                 UpdateExpression="set #c=:c, #n=:n #ef=:ef #ex=:ex",
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

    def delete(self):
        return table.delete_item(Key=self.Key)

    def getall(self):
        return table.query(
            IndexName='ItemTypes',
            KeyConditionExpression=Key('ItemType').eq(self.ItemType))


def branchcreate(event, context):
    dto = Branch(event['queryStringParameters'])
    ret_val = dto.create()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def branchupdate(event, context):
    dto = Branch(event['queryStringParameters'])
    ret_val = dto.update()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def branchread(event, context):
    item = event['queryStringParameters']
    dto = Branch(item)
    ret_val = dto.read()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def branchlistall(event, context):
    dto = Branch(None)
    ret_val = dto.getall()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response


def branchdelete(event, context):
    dto = Branch(event['queryStringParameters'])
    ret_val = dto.delete()
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': ret_val})
    }
    return response
