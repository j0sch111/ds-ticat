import json

import lambda_handler
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_request():
    raw_data = request.get_data(as_text=True)
    event = {"body": raw_data}
    context = {}

    # Call the lambda_handler function
    result = lambda_handler.lambda_handler(event, context)
    if isinstance(result["body"], str):
        result["body"] = json.loads(result["body"])

    # Return the result
    return jsonify(result["body"]), result["statusCode"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
