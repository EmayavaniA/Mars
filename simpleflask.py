import json
from flask import Flask,request



app = Flask(__name__)


@app.route("/hello")
def hello_world():
        return "<p>Hello, World!</p>"
  
@app.route('/Controller', methods=['POST'])
def Controller():
    try:
        json_data =request.get_json()
        print("Hello")
        #useCaseType = json_data['useCaseType']
        #print(useCaseType)
        json_dict = json.dumps(json_data)
        print(json_data)
        return json_dict
    except Exception as e:
        raise Exception(e)
        #sys.exit(1)

if __name__ == '__main__':
        app.run(host='0.0.0.0',debug=True, port=8080)





