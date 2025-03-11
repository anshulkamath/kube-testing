from flask import Flask, request, jsonify
import numpy as np
import aiohttp
import asyncio
import os

app = Flask(__name__)

COMPUTE_SERVICE_ENDPOINT = os.environ.get("COMPUTE_SERVICE_ENDPOINT", "http://0.0.0.0:8001/dotProduct")
PORT = int(os.environ.get("PORT", 8000))

async def submit_requests(url, request_data):
  async with aiohttp.ClientSession() as session:
    requests = [
        session.post(url=url, json=r)
        for r in request_data
    ]

    responses = await asyncio.gather(*requests, return_exceptions=True)

    result = []
    for r in responses:
      result.append(await r.json())
    return result


@app.route('/', methods=['GET'])
def ping():
  return "server ping pong", 200


@app.route('/multiply', methods=['POST'])
def multiply():
  try:
    data = request.get_json()

    mat1 = data["mat1"]
    mat2 = np.transpose(data["mat2"]).tolist()
    mats = ({ "x": r1, "y": r2 } for r1 in mat1 for r2 in mat2)

    responses = asyncio.run(submit_requests(COMPUTE_SERVICE_ENDPOINT, mats))
    flat_dot_products = list(map(lambda x: x["dotProduct"], responses))

    matrix = np.reshape(flat_dot_products, (len(mat1), len(mat2))).tolist()

    return jsonify({
      "dotProduct": matrix
      }), 200

  except Exception as e:
    return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
  if not COMPUTE_SERVICE_ENDPOINT:
    raise ValueError("must define COMPUTE_SERVICE_ENDPOINT")

  print(f"using {COMPUTE_SERVICE_ENDPOINT}")
  port = PORT
  app.run(host='0.0.0.0', port=port)
