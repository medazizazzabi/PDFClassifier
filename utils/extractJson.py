import requests
apikey = ""
baseUrl = "https://ws.beta.machine-editique.neopolis-dev.com/"
def extractJson(_id):
    url = baseUrl+"editique_pdf/get_pdf_fields_by_doc_id/"+_id
    headers = {'Apikey': apikey}
    response = requests.get(url, headers=headers)
    return response.json()

def saveJson(_id):
    jsonR = extractJson(_id)
    name = jsonR['modelName']
    jsonText = jsonR['fieldsIds']
    url = jsonR['fileUrl'].replace("./", baseUrl)
    #donwload pdf from url
    with open(name+".json", "w") as f:
        f.write(jsonText)
    
    with open(name+".pdf", "wb") as f:
        f.write(requests.get(url).content)

if __name__ == "__main__":
    pdfid = input("Enter pdf id: ")
    saveJson(pdfid)
    
    


