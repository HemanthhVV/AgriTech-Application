import boto3,os,cv2,re

class ProcessImage:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=os.environ.get('AWS_ACCESS_ID'),
            aws_secret_access_key=os.environ.get('AWS_PASS_KEY'),
            region_name=os.environ.get('REGION')
        )
        self.client = self.session.client('textract',region_name=os.environ.get('REGION'))

    def preprocessimage(self,image_path,image_name):
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        height,width = img.shape
        roi = img[int(height * 0.5) : height,0:int(width*0.7)]
        _, encoded_image = cv2.imencode('.jpg', roi)

        # Return the encoded image as bytes
        return encoded_image.tobytes()

    def processingImage(self,image_path:str,image_name:str):
        # Tries as possibilty
        # with open(image_path,'rb') as file:
        #     image = file.read()
        #     image = self.preprocessimage(image)
        byte_image = self.preprocessimage(image_path=image_path,image_name=image_name)
        # byte_image = bytearray(image)
        print(f'file loaded ----> {image_path}')
        response = self.client.detect_document_text(Document={"Bytes": byte_image})
        temp =[]
        for i in response['Blocks']:
            if i['BlockType'] == 'LINE':
                temp.append(i['Text'])
        return temp

    def getCoordinates(self,sentence):
        latitude_pattern = re.compile(r'lat(?:itude)?\s*:\s*([-+]?\d*\.\d+|\d+)')
        latitude_pattern2 = re.compile(r'at(?:itude)?\s*:\s*([-+]?\d*\.\d+|\d+)')
        longitude_pattern = re.compile(r'long(?:itude)?\s*:\s*([-+]?\d*\.\d+|\d+)')

        # Initialize variables to store the results
        latitude = None
        longitude = None

        # Search for latitude and longitude in the array
        for item in sentence:
            lat_match = latitude_pattern.search(item)
            lat_match2 = latitude_pattern2.search(item)
            long_match = longitude_pattern.search(item)

            if lat_match:
                latitude = lat_match.group(1)  # Extract the latitude value
            if lat_match2 and latitude is not None:
                latitude = lat_match2.group(1)  # Extract the latitude value
            if long_match:
                longitude = long_match.group(1)  # Extract the longitude value
        
        return [latitude,longitude]

