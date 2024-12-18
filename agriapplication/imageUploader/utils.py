import boto3,os,cv2,re,string

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
        sentence = list(map(lambda x:x.lower(),sentence))
        latitude_pattern = re.compile(r'(l*atitude:\s*[0-9]*\.[0-9]*)|([la]*titude:\s[0-9]*\.[0-9]*)')
        longitude_pattern = re.compile(r'([lon]*gitude:\s*[0-9]*\.[0-9]*)|(long*titude:\s[0-9]*\.[0-9]*)')
        time_pattern = re.compile(r'(t*ime:\s*[0-9]*\-*[0-9]*\-*[0-9]*\s*[0-9]*\:*[0-9]*)|([ti]*me:\s*[0-9]*\-*[0-9]*\-*[0-9]*\s*[0-9]*\:*[0-9]*)|([tim]*e:\s*[0-9]*\-*[0-9]*\-*[0-9]*\s*[0-9]*\:*[0-9]*)')
        farmerID_pattern = re.compile(r'[A-Z]*[a-z]*[\s\-:]*(farmer)[\s\-:]*i*[\s\':]*d*[\s:\-]*\d+\b')
        farmer_name_pattern = re.compile(r'f*armer\s*(name)*[\s\-:]*[a-z\s]*')


        # Initialize variables to store the results
        latitude = None
        longitude = None
        time_uploaded,timeMxSpan = None,0
        farmerID,idMxSpan = None,0
        farmer_name,nameMxSpan = None,0

        # Search for latitude and longitude in the array
        for item in sentence:
            lat_match = latitude_pattern.search(item)
            long_match = longitude_pattern.search(item)
            time_match = time_pattern.search(item)
            farmerID_match = farmerID_pattern.search(item)
            farmer_name_match = farmer_name_pattern.search(item)

            if lat_match:
                latitude = lat_match.group() # Extract the latitude value
            if long_match:
                longitude = long_match.group()  # Extract the longitude value
            if time_match:
                l,r = time_match.span()
                if (r-l) > timeMxSpan:
                    time_uploaded = time_match.group()
                    timeMxSpan = (r-l)
            if farmerID_match:
                # print(farmerID_match)
                l,r = farmerID_match.span()
                if (r-l) > idMxSpan:
                    farmerID = farmerID_match.group()
                    idMxSpan = (r-l)
            if farmer_name_match:
                l,r = farmer_name_match.span()
                if (r-l) > nameMxSpan:
                    farmer_name = farmer_name_match.group()
                    nameMxSpan = (r-l)

            # print(latitude,longitude)

        return [latitude,longitude,time_uploaded,farmerID,farmer_name]


    def makePreciseText(self,s):
        res = []
        punctuations = set(string.punctuation)
        for i,word in enumerate(s):
            if i == 1:
                temp = []
                for ch in word:
                    if ch.isdigit():
                        temp.append(ch)
                res.append(''.join(temp))
            else:
                index = 0
                while index < len(word) and word[index] not in punctuations:
                    index+=1
                res.append(None if index >= len(word) else str(word[index+1:].strip()))
        if not res[0] or len(res[0]) < 4:
            res[0] = 'Does not able to parse'
        if not res[2] or len(res[0]) < 4:
            res[2] = 'Does not able to parse'
        return res