from flask import Flask, request, jsonify
import numpy as np
import os

app = Flask(__name__)


PORT = int(os.environ.get("PORT", 8001))

@app.route('/', methods=['GET'])
def ping():
  return "worker pong", 200


@app.route('/dotProduct', methods=['POST'])
def dot_product():
  try:
    data = request.get_json()
    print(data)

    return jsonify({
      "dotProduct": np.dot(data["x"], data["y"]).item(),
    }), 200

  except Exception as e:
    return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    port = PORT
    app.run(host='0.0.0.0', port=port)

