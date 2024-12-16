import boto3,os

class ProcessImage:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=os.environ.get('AWS_ACCESS_ID'),
            aws_secret_access_key=os.environ.get('AWS_PASS_KEY'),
            region_name=os.environ.get('REGION')
        )
        self.client = self.session.client('textract')

    def processingImage(self,image_path:str):
        with open(image_path,'rb') as file:
            image = file.read()
            byte_image = bytearray(image)
            print(f'file loaded ----> {image_path}')
        response = self.client.detect_document_text(Document={"Bytes": byte_image})
        temp =[]
        for i in response['Blocks']:
            if i['BlockType'] == 'LINE':
                temp.append(i['Text'])
        return temp
