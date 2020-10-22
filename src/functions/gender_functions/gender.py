import uuid
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', endpoint_url='http://host.docker.internal:8000')
table = dynamodb.Table('ReferenceData')
item_type = 'GENDER'


class Gender:
    def __init__(self, item):
        if item is not None:
            self.ItemUUID = item.get('ItemUUID')
            self.Code = item.get('Code')
            self.Name = item.get('Name')
            self.EffectiveDate = item.get('EffectiveDate', None)
            self.ExpirationDate = item.get('ExpirationDate', None)
            print(self.EffectiveDate)
            print(self.ExpirationDate)
            self.Key = {'ItemUUID': self.ItemUUID, 'ItemType': item_type}

    def create(self):
        if self.ItemUUID is None:
            self.ItemUUID = str(uuid.uuid4())
        return table.put_item(Item={'ItemUUID': self.ItemUUID, 'ItemType': item_type,
                                    'Code': self.Code, 'Name': self.Name,
                                    'EffectiveDate': self.EffectiveDate, 'ExpirationDate': self.ExpirationDate})

    def read(self):
        return table.get_item(Key=self.Key)

    def update(self):
        return table.update_item(Key=self.Key,
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

    def delete(self):
        return table.delete_item(Key=self.Key)

    def getall(self):
        return table.query(
            IndexName='item-type-index',
            KeyConditionExpression=Key('ItemType').eq(item_type))

