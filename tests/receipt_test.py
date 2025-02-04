import pytest
from models.receipt import Receipt
from models.item import Item

@pytest.mark.parametrize(
	"retailer,purchase_date,purchase_time,items,total",
	[
		(
			"Target",
			"2022-01-02",
			"13:13",
			[{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
			"1.25"
		),
		(
			"Walgreens",
			"2022-01-02",
			"08:13",
			[{"shortDescription": "Pepsi - 12-oz", "price": "1.25"},{"shortDescription": "Dasani", "price": "1.40"}],
			"2.65"
		)
	]
)
def test_receipt(retailer, purchase_date, purchase_time, items, total):
	datum = {
		"retailer": retailer,
		"purchaseDate": purchase_date,
		"purchaseTime": purchase_time,
		"items": items,
		"total": total
		}
	receipt = Receipt(datum)
	assert receipt is not None
	assert receipt.retailer == retailer
	assert receipt.purchase_date == purchase_date
	assert receipt.purchase_time == purchase_time
	assert receipt.total == total
	item = receipt.items[0]
	assert item is not None
	assert isinstance(item, Item)
	assert item.short_description == items[0]["shortDescription"]
	assert item.price == items[0]["price"]
