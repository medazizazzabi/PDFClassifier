
import json

def getData(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def cleanUpFields(data):
    removeList=['id','type','size','lineHeight','fontFamily','fieldType','TextFormat','FormatCode','charactersNumber','visibility','relation','color']
    output = []

    for index,page in enumerate(data):
        for field in page:
            field['page']=index
            field['appended']=False
            [field.pop(key) for key in removeList]
            output.append(field)
    return output

def createClassification(categories,fields):
    for category in categories:
        category['fields']=[]
    categories  = sorted(categories,key=lambda k:k['y']+k['page']*1000,reverse=True)
    for field in fields:
        for category in categories:
            if (field['appended']==False) and (field['y']+1000*field['page']) > (category['y']+1000*category['page']):
                field['appended']=True
                category['fields'].append(field)


    return sorted(categories,key=lambda k:k['y']+k['page']*1000)

def saveResults(res):
    with open('result.json', 'w') as fp:
        json.dump(res, fp,indent=4)

def classify(categories,fields):
    cleanFields = cleanUpFields(fields)

    classification=createClassification(categories,cleanFields)
    return classification


if __name__ == '__main__':
    categories = getData('categories.json')
    fields = getData('fields.json')
    result = classify(categories,fields)
    saveResults(result)
    print(result)