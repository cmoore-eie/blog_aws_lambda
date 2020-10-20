import uuid
import boto3


def create_reference_table(dynamodb=None):

    '''
    Delete the existing table if any, this allows the process to work at cleaning up
    and restarting from the beginning.
    '''
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    try:
        del_table = dynamodb.Table('ReferenceData').delete()
    except:
        pass

    '''
    The table is created with a single GSI, and only the primary key defined
    '''
    table = dynamodb.create_table(
        TableName='ReferenceData',
        KeySchema=[
            {
                'AttributeName': 'ItemUUID',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'ItemType',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ItemUUID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'ItemType',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'item-type-index',
                'KeySchema': [
                    {
                        'AttributeName': 'ItemType',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            }]
    )

    '''
    The client is extracted and used to update the table adding the second GSI
    '''
    dynamodb.meta.client.update_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'ItemUUID',
                'AttributeType': 'S'
            }
        ], TableName='ReferenceData',
        GlobalSecondaryIndexUpdates=[
            {'Create': {
                'IndexName': 'item-uuid-index',
                'KeySchema': [
                    {
                        'AttributeName': 'ItemUUID',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            }}])

    '''
    The sample data is created for Gender, Branch and Dealer
    '''
    table.put_item(Item={'ItemUUID': str(uuid.uuid4()),
                         'ItemType': 'GENDER',
                         'Code': 'm',
                         'Name': 'Male',
                         'EffectiveDate': '2020-01-01'})
    table.put_item(Item={'ItemUUID': str(uuid.uuid4()),
                         'ItemType': 'GENDER',
                         'Code': 'f',
                         'Name': 'Female',
                         'EffectiveDate': '2020-01-01'})
    table.put_item(Item={'ItemUUID': str(uuid.uuid4()),
                         'ItemType': 'BRANCH',
                         'Code': 'b1',
                         'Name': 'Branch 1',
                         'BranchType': 'Local',
                         'EffectiveDate': '2020-01-01'})
    table.put_item(Item={'ItemUUID': str(uuid.uuid4()),
                         'ItemType': 'BRANCH',
                         'Code': 'b2',
                         'Name': 'Branch 2',
                         'BranchType': 'Main',
                         'EffectiveDate': '2020-01-01'})
    dealeruuid = str(uuid.uuid4())
    table.put_item(Item={'ItemUUID': dealeruuid,
                         'ItemType': 'DEALER',
                         'Code': 'd1',
                         'Name': 'Dealer 1',
                         'EffectiveDate': '2020-01-01'})
    table.put_item(Item={'ItemUUID': dealeruuid,
                         'ItemType': 'DEALER_LOCATION#' + str(uuid.uuid4()),
                         'Name': 'Dealer 1 Location',
                         'AddressLine1': '123 Main Street',
                         'AddressLine2': 'Orange',
                         'City': 'London'})
    table.put_item(Item={'ItemUUID': dealeruuid,
                         'ItemType': 'DEALER_LOCATION#' + str(uuid.uuid4()),
                         'Name': 'Dealer 1 Location',
                         'AddressLine1': '1 South Street',
                         'AddressLine2': 'Apple',
                         'City': 'London'})

    return table


if __name__ == '__main__':
    reference_table = create_reference_table()
    print("Table status:", reference_table.table_status)
