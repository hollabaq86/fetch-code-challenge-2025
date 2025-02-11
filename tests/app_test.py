# make sure we have correct path to import flask app
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from app import create_app, validate_request_data
import pytest

@pytest.fixture()
def app():
	app = create_app()
	app.config.update({
        "TESTING": True,
    })
	return app

@pytest.fixture()
def client(app):
	return app.test_client()

@pytest.fixture()
def receipt_id(client):
	request_data = {
		"retailer": "Walgreens",
		"purchaseDate": "2022-01-02",
		"purchaseTime": "08:13",
		"items": [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"},{"shortDescription": "Dasani", "price": "1.40"}],
		"total": "2.65",
	}
	response = client.post("/receipts/process", json=request_data)
	return response.json["id"]

def test_post_process_receipt_single_item(client):
	request_data = {
		"retailer": "Walgreens",
		"purchaseDate": "2022-01-02",
		"purchaseTime": "08:13",
		"items": [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"},{"shortDescription": "Dasani", "price": "1.40"}],
		"total": "2.65",
	}
	response = client.post("/receipts/process", json=request_data)
	assert response.status_code == 200
	assert response.data is not None
	assert "id" in response.json

def test_post_process_receipt_multi_items(client):
	request_data = {
    "retailer": "Walgreens",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "08:13",
    "total": "2.65",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
        {"shortDescription": "Dasani", "price": "1.40"}
    	],
	}
	response = client.post("/receipts/process", json=request_data)
	assert response.status_code == 200
	assert response.data is not None
	assert "id" in response.json

def test_post_process_receipt_bad_data(client):
	request_data = {
    "retailer": "Walgreens",
    "notValid": "2022-01-02",
    "purchaseTime": "08:13",
    "total": "2.65",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
        {"shortDescription": "Dasani", "price": "1.40"}
    	],
	}
	response = client.post("/receipts/process", json=request_data)
	assert response.status_code == 400
	assert "The receipt is invalid." in str(response.data)
	assert response.json is None

def test_get_points(client, receipt_id):
	url = "/receipts/" + receipt_id + "/points"
	response = client.get(url)
	assert response.status_code == 200
	assert response.data is not None
	assert response.json["points"] == 15

def test_get_points_no_receipt(client):
	response = client.get("/receipts/bad-id/points")
	assert response.status_code == 404
	assert "No receipt found for that ID." in str(response.data)
	assert response.json is None

@pytest.mark.parametrize(
	"datum,is_valid",
	[
		(
			{
			    "retailer": "Walgreens",
			    "purchaseDate": "2022-01-02",
			    "purchaseTime": "08:13",
			    "total": "2.65",
			    "items": [
			        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
			        {"shortDescription": "Dasani", "price": "1.40"}
			    	],
			},
			True
		),
		(
			{
			    "retailer": "Walgreens",
			    "purchaseDate": "2022-01-02",
			    "total": "2.65",
			    "items": [
			        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
			        {"shortDescription": "Dasani", "price": "1.40"}
			    	],
			},
			False
		),
		(
			{
			    "retailer": "Walgreens",
			    "purchaseDate": "2022-01-02",
			    "notValid": "08:13",
			    "total": "2.65",
			    "items": [
			        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
			        {"shortDescription": "Dasani", "price": "1.40"}
			    	],
			},
			False
		),
		(
			{
			    "retailer": "Walgreens",
			    "purchaseDate": "2022-01-02",
			    "purchaseTime": "08:13",
			    "total": "2.65",
			    "items": [],
			},
			False
		),
		(
			{
			    "retailer": "Walgreens",
			    "purchaseDate": "2022-01-02",
			    "purchaseTime": "08:13",
			    "total": "2.65",
			    "items": [
			        {"shortDescription": "Pepsi - 12-oz"},
			        {"shortDescription": "Dasani", "price": "1.40"}
			    	],
			},
			False
		),
		(
			{
			    "retailer": "Walgreens",
			    "purchaseDate": "2022-01-02",
			    "purchaseTime": "08:13",
			    "total": "2.65",
			    "items": [
			        {"shortDescription": "Pepsi - 12-oz", "notValid": "1.25"},
			        {"shortDescription": "Dasani", "price": "1.40"}
			    	],
			},
			False
		),
	]
)
def test_validate_request_data(datum, is_valid):
	validation_result = validate_request_data(datum)
	assert validation_result == is_valid

