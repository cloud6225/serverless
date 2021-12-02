from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json

print('Loading function')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print("yoo>>>",event)
    print("event>>>",type(event))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)
    print("message>>>",type(message))
    sendEmail(message)
    return message


def sendEmail(message):    
    message = json.loads(message)
    # This address must be verified with Amazon SES.
    SENDER = "noreply@prod.mrudulladhwe.me"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = message['email']

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "Account Verification Email"

    url = "http://api.prod.mrudulladhwe.me/v1/verifyUserEmail?email="+RECIPIENT+"&token="+ message['token']

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Hello\r\n"
                "We just need to verify your email address before you can access the application"
                "CLink the below link to verify your account"+
                url
                )
            
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h2>Verify Account</h2>
    <p>"We just need to verify your email address before you can access the application"</p>
    <p>Kindly, Click the below link to verify your account
        <a href='"""+url+"""'>
        """+url+"""</a>.</p>
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)


    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])