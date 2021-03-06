import json
import os
import boto3
from todos import decimalencoder

# AWS service to translate
traductor = boto3.client(service_name='translate')
dynamodb = boto3.resource('dynamodb')


# Function that translate the field text register from bd to other language
def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    # get register by id from bbdd
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    # include language to translate
    idioma= event['pathParameters']['idioma']
    
    # Get text from register and translate via aws service
    texto=result['Item']['text']
    traduccion = traductor.translate_text(Text=texto, SourceLanguageCode="es", TargetLanguageCode=idioma)
    
    # json response
    response = {
        "statusCode": 200,
        "body": json.dumps(traduccion, cls=decimalencoder.DecimalEncoder)
    }

    return response
