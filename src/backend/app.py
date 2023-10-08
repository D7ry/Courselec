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
    # Sample data as a list of dictionaries
    data = [
        {'id': 1, 'name': 'Item 4'},
        {'id': 2, 'name': 'Item 5'},
        {'id': 3, 'name': 'Item 6'}
    ]

    from time import sleep
    sleep(0.5)
    # Return the data as a JSON response
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)