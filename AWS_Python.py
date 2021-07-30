import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name = helper.region)

table = dynamodb.Table(helper.TableName)

### Insert Item
Item = {
                'PredictionID': generateId,
                'Title': request.json.get('Title').strip(),
                'UniqueTitle': request.json.get('Title').strip().upper(),
                'Authors': request.json.get('Authors'),
                'IsPublishPrediction': isPublishPrediction,
                'IsNewDraftAvailable': "False",
                'Workstreams': request.json.get('Workstreams')
                }
result = table.put_item(Item=Item)


### Scan Item

response = table.scan(
    ProjectionExpression=ListofAttributeNames,
    FilterExpression=Attr("AttributeName1").contains("VALUE1") & Attr(
        "AttributeName2").eq("VALUE2"))
data = response['Items']

while response.get('LastEvaluatedKey'):
    response = table.scan(
        ProjectionExpression=ListofAttributeNames,
        FilterExpression=Attr("AttributeName1").contains(VALUE1) & Attr(
            "AttributeName2").eq("VALUE2"),
        ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])

data = jsonpickle.encode(data, unpicklable=False)



### Update Item

response = table.update_item(
                Key={
                    'AttributeID': Id
                },
                UpdateExpression="set #attrName = :attrValue, AttrName1 =:Attr1, AttrName "
                                    "= list_append(AttrName, :Attr2)",
                ExpressionAttributeNames={
                    "#attrName": "attrNameValue"
                },
                ExpressionAttributeValues={
                    ':attrValue':
                        attrValueData,
                    ':Attr1':
                        Attr1Value,
                    ":Attr2": [
                        Attr2Value
                    ]
                },
            )

table.update_item(
                Key={
                    'AttributeID': Id
                },
                UpdateExpression='DELETE Attr1 :Attr1Value, Attr2 :Attr2Value',
                ExpressionAttributeValues={":Attr1Value": set(Attr1Value),
                                           ":Attr2Value": set(Attr2Value)
                                           })

table.update_item(
    Key={
        'AttributeID': Id
    },
    UpdateExpression='ADD Attr1 :Attr1Value, Attr2 :Attr2Value',
    ExpressionAttributeValues={":Attr1Value": set(Attr1Value),
                                ":Attr2Value": set(Attr2Value)
                                })

### Query Item

response = table.query(
                ProjectionExpression='Attr1, Attr2, Attr3, Attr4, Attr5',
                KeyConditionExpression=Key('AttributeID').eq(Id)
            )
