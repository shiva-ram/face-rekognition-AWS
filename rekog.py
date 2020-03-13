def lambda_handler(event, context):
    import boto3
    import json
    from boto3.dynamodb.conditions import Key, Attr
    from datetime import datetime,timedelta
    from pytz import timezone
   
        
    s3 = boto3.resource('s3')
    for record in event['Records']:
        BUCKET1 = "#your_Targetbucket_name"
        KEY_TARGET =record['s3']['object']['key'] 
        print(KEY_TARGET)
        def compare_faces(bucket, key, bucket_target, key_target,threshold=60, region="us-east-1"):
            rekognition = boto3.client("rekognition", region)
            response = rekognition.compare_faces(
                SourceImage={
                    "S3Object": {
                        "Bucket": bucket,
                        "Name": key,
                        
                    }
                    
                },
                TargetImage={
                    "S3Object": {
                        "Bucket": bucket_target,
            			"Name": key_target,
                        
                    }
                    
                }
            )
            return response['SourceImageFace'], response['FaceMatches']
            
        
        #print(BUCKET)
        #print(BUCKET1)
        #print(KEY_TARGET)
        
        BUCKET = s3.Bucket('#your_sourcebucket_name')
            #print(BUCKET1.name)
        for s3_object in BUCKET.objects.all():
            KEY_SOURCE=s3_object.key
            print(KEY_SOURCE)
            source_face, matches = compare_faces(BUCKET.name, KEY_SOURCE, BUCKET1, KEY_TARGET)
                            
            # the main source face
            print ("Source Face ({Confidence}%)".format(**source_face))
                            
            # one match for each target face
            for match in matches:
                print ("Target Face ({Confidence}%)".format(**match['Face']))
                x = "{}".format(match['Similarity'])
                similarity = float(x)
                if similarity >= 80:
                    print(KEY_SOURCE)
                    now_utc=datetime.now(timezone('Asia/Kolkata'))
                    now_culcutta=now_utc.astimezone(timezone('Asia/Kolkata'))
                    date1 = now_utc.strftime("%x")
                    time1 = now_utc.strftime("%X")
                    s2 = boto3.resource('s3')
                    s3 = boto3.client('s3')
        
                    url='{}/{}/{}'.format(s3.meta.endpoint_url,BUCKET.name,KEY_SOURCE)
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('#sourcetablename')
        response = table.scan(ProjectionExpression = "#sourcetable_key_src")
        for i in response['Items']:
            data='{img_src}'.format(**i)
            if data == url:
                dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
                table = dynamodb.Table('#sourcetablename')
                response = table.query(
                    KeyConditionExpression=Key('#sourcetable_key_src').eq(data)
                    )
                items = response['Items']
                
                for x in range(len(items)):
                    name=items[x]['name_1']
                    id=items[x]['id']
                    print(name)
                    print(id)
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('#finaltablename')
                table.put_item(
                    Item={
                        'nam': name,
                        'id': id,
                        'date_1':date1,
                        'tym_1':time1
                        }
                    )
                print('success')
            else:
                print('notsucces')
                            	
        s3 = boto3.resource('s3')
        s3.Object('#your_Targetbucket_name','Key').delete()  
        
