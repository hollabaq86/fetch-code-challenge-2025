from flask import Flask
from flask import request
from models.receipt import Receipt

app = Flask(__name__)

receipts = {}

@app.post("/receipts/process")
def process():
    datum = request.get_json()
    if "retailer" in datum.keys():
        receipt = Receipt(datum)
        receipts[receipt.id] = receipt
    return {"id": receipt.id}

@app.get("/receipts/<id>/points")
def get_points(id):
    receipt_id = id
    return {"points": receipts[receipt_id].points}

def create_app():
    return app
