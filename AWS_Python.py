import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name = helper.region)

table = dynamodb.Table(helper.PredictionTableName)

### Insert Item
PredictionItem = {
                'PredictionID': generatePredictionId,
                'Title': request.json.get('Title').strip(),
                'UniqueTitle': request.json.get('Title').strip().upper(),
                'Authors': request.json.get('Authors'),
                'IsPublishPrediction': isPublishPrediction,
                'IsNewDraftAvailable': "False",
                'Workstreams': request.json.get('Workstreams')
                }
result = table.put_item(Item=PredictionItem)


### Scan Item

response = table.scan(
    ProjectionExpression=predictionItemListForAllPrediction,
    FilterExpression=Attr("BrainTrustReviewPendingUsers").contains(brainTrustUserName) & Attr(
        "PredictionStatus").eq("Active"))
data = response['Items']

while response.get('LastEvaluatedKey'):
    response = table.scan(
        ProjectionExpression=predictionItemListForAllPrediction,
        FilterExpression=Attr("BrainTrustReviewPendingUsers").contains(brainTrustUserName) & Attr(
            "PredictionStatus").eq("Active"),
        ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])

data = jsonpickle.encode(data, unpicklable=False)



### Update Item

response = table.update_item(
                Key={
                    'PredictionID': generatePredictionId
                },
                UpdateExpression="set #attrName = :attrValue, IsNewDraftAvailable =:IsNewDraftAvailable, Versioning "
                                    "= list_append(Versioning, :Version)",
                ExpressionAttributeNames={
                    "#attrName": "Draft"
                },
                ExpressionAttributeValues={
                    ':attrValue':
                        draftData,
                    ':IsNewDraftAvailable':
                        isNewDraftAvailable,
                    ":Version": [
                        predictionVersionData
                    ]
                },
            )

table.update_item(
                Key={
                    'PredictionID': generatePredictionId
                },
                UpdateExpression='DELETE BrainTrustUsers :AddBrainTrustUsers, BrainTrustReviewPendingUsers :PendingUsers',
                ExpressionAttributeValues={":AddBrainTrustUsers": set(existingBrainTrustUser),
                                           ":PendingUsers": set(existingBrainTrustUser)
                                           })

table.update_item(
    Key={
        'PredictionID': generatePredictionId
    },
    UpdateExpression='ADD BrainTrustUsers :AddBrainTrustUsers, BrainTrustReviewPendingUsers :PendingUsers',
    ExpressionAttributeValues={":AddBrainTrustUsers": set(BrainTrustUsers),
                                ":PendingUsers": set(BrainTrustUsers)
                                })

### Query Item

response = table.query(
                ProjectionExpression='Authors, CreatedByUserName,OwnerNTID, CreatedByNTID, Title',
                KeyConditionExpression=Key('PredictionID').eq(predictionId)
            )