from flask import Flask
from flask import abort, request
from models.receipt import Receipt
from typing import Dict

app = Flask(__name__)

receipts = {}

ACCEPTABLE_RECEIPT_KEYS = set(["retailer","purchaseDate","purchaseTime","items","total"])
ACCEPTABLE_ITEM_KEYS = set(["shortDescription","price"])

@app.post("/receipts/process")
def process():
    datum = request.get_json()
    validation_result = validate_request_data(datum)
    if not validation_result:
        abort(400, description="The receipt is invalid.")
    receipt = Receipt(datum)
    receipts[receipt.id] = receipt
    return {"id": receipt.id}

@app.get("/receipts/<id>/points")
def get_points(id):
    receipt_id = id
    if receipt_id not in receipts:
        abort(404, description="No receipt found for that ID.")
    return {"points": receipts[receipt_id].points}

def validate_request_data(datum: Dict):
    request_keys = set(datum.keys())
    bad_keys = ACCEPTABLE_RECEIPT_KEYS.difference(request_keys)
    if len(bad_keys) > 0:
        return False
    if len(datum["items"]) == 0:
        return False
    for item in datum["items"]:
        request_item_keys = set(item.keys())
        bad_keys = ACCEPTABLE_ITEM_KEYS.difference(request_item_keys)
        if len(bad_keys) > 0:
            return False
            break
    return True

def create_app():
    return app
