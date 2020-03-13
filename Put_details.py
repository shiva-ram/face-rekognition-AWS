def lambda_handler(event, context):
    import boto3
    import json
    import decimal
    from boto3.dynamodb.conditions import Key, Attr
    
    s3 = boto3.resource('s3')
    bucket_name = '#your_sourcebucket_name'
    
    s2 = boto3.resource('s3')
    s3 = boto3.client('s3')
    
    #image retrieval
    img = '{}'.format(event["photo"])
    object = s2.Bucket(bucket_name).Object(img)
    
    #converting image to specific path and permission
   
    object.Acl().put(ACL='public-read')
    
    #Getting Registration part details
    result='{}'.format(event["result"])
    content = json.dumps(eval(result))
    final = json.loads(content)
    print(s3.meta.endpoint_url)
    url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket_name, img)
    
    name = final["name"]
    phone = final["phone"]
    address = final["address"]
    std_id = final["sid"]
  
    #storing Registration and image path to dynamodb
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('#sourcetablename')


    response = table.put_item(
        Item={
            'name_1':name,
            'phone':phone,
            'address':address,
            'id':std_id,
            'img_src':url
        }
        )