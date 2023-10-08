from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "Hello, World!3"

@app.route("/test/")
def test():
    return "test"

@app.route("/test2/")
def test2():
    return "test2"


@app.route('/data/')
def get_data():
    # Create a dictionary with data to return as JSON
    data = {
        'message': 'This is data from the /data endpoint on the Flask backend.'
    }
    
    # Return the data as JSON
    return jsonify(data)

@app.route('/course_advisor/query/', methods=['GET'])
def query_advisor():
    param = request.args.get('param')
    ret = {
        "param" : param,
        "values" :
            [
                "CS 101",
                "CS 102",
                "CS 103"
            ]
    }
    return jsonify(ret)

if __name__ == "__main__":
    app.run(debug=True)