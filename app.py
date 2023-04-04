import json

#from flask import Flask, request
from flask import Flask, jsonify, request
app = Flask(__name__)
import pandas as pd
import os
import joblib



def get_vectorizer():
    folder_path='C:/Users/rafiqul.islam/IdeaProjects/untitled7/data'
    vec = "vectorizer.pickle"
    vpath = os.path.join(folder_path, vec)
    return joblib.load(vpath)

def get_classifier():
    folder_path='C:/Users/rafiqul.islam/IdeaProjects/untitled7/data'
    clf = "classifier.pickle"
    clfPath = os.path.join(folder_path, clf)
    return joblib.load(clfPath)

def predict2(userInput):
    folder_path='C:/Users/rafiqul.islam/IdeaProjects/untitled7/data'
    if not isinstance(userInput, str):
        raise ValueError("Input should be a string")
    #folder_path = os.path.join(".", "modelStudy")  # Assumes that modelStudy is in the same directory
    vectorizer = get_vectorizer()
    classifier = get_classifier()
    if vectorizer and classifier is not None:
        transformedInput = vectorizer.transform([userInput])
        print(transformedInput)
        prediction = classifier.predict(transformedInput)
        print(prediction)
        return prediction.tolist()
    else:
        return []
def get_findvalue(val):
    df=pd.read_csv('C:/Users/rafiqul.islam/Desktop/modelStudy/classes.csv')
    dict_data = dict(zip(df.classID, df.Classification))
    #print(dict_data[val])
    return dict_data[val]

@app.route('/example', methods=['POST'])
def example():

    # get request body as a string
    body_str = request.data.decode('utf-8')

    # convert string to dictionary using json.loads()
    body_dict = json.loads(body_str)
    data=body_dict['message']
    pre=predict2(data)
    preresult=pre[0]

    new_data=get_findvalue(preresult)
    newdict={'result':new_data}
    print(newdict)
    return jsonify(newdict)


@app.route('/api/data', methods=['GET', 'POST', 'OPTIONS'])
def data():
    if request.method == 'OPTIONS':
        # Set CORS headers for preflight request
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        print(type(request.data))
        print(request.data)
        # get request body as a string
        body_str = request.data.decode('utf-8')

        # convert string to dictionary using json.loads()
        body_dict = json.loads(body_str)
        data=body_dict['message']
        pre=predict2(data)
        preresult=pre[0]

        new_data=get_findvalue(preresult)
        newdict={'result':new_data}
        print(newdict)
        return jsonify(newdict)
        #return jsonify({'success': True})
    elif request.method == 'POST':
        body_str = request.data.decode('utf-8')

        # convert string to dictionary using json.loads()
        body_dict = json.loads(body_str)
        data=body_dict['message']
        pre=predict2(data)
        preresult=pre[0]

        new_data=get_findvalue(preresult)
        newdict={'result':new_data}
        print(newdict)
        return jsonify(newdict)


    else:
        # Handle GET request and return response
        return jsonify({'data': 'please change it post method'})

@app.route('/')
def hello_world():  # put application's code here
    return {'message': 'Hello World'}



if __name__ == '__main__':
    app.run(port=5000, debug=False)
