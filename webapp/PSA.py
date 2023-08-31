import requests, json
from utils import convertPDF2IMG

class PSA:
    def __init__(self,api_key,_id,name) -> None:
        self.baseUrl = "https://ws.beta.machine-editique.neopolis-dev.com/"
        self.apikey = api_key
        self._id = _id
        self.jsonFields = {}
        self.jsonImages = {}
        self.saveJson(name)

    def extractJson(self):
        url = self.baseUrl+"editique_pdf/get_pdf_fields_by_doc_id/"+self._id
        headers = {'Apikey': self.apikey}
        response = requests.get(url, headers=headers)
        return response.json()

    def saveJson(self,name):
        jsonR = self.extractJson()
        url = jsonR['fileUrl'].replace("./", self.baseUrl)
        #convert jsonR['fieldsIds'] to json
        self.jsonFields = json.loads(jsonR['fieldsIds'])
        self.jsonImages = convertPDF2IMG(requests.get(url).content,name)