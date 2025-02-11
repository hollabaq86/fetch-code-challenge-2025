import pytest
from models.item import Item

@pytest.mark.parametrize(
	"description,price",
	[
		("foo","6.49"),
		("bar","10.32"),
		("this is a short description","0.00"),
	]
)
def test_item(description, price):
	datum = {"shortDescription": description, "price": price}
	item = Item(datum)
	assert item is not None
	assert item.short_description == description
	assert item.price == float(price)

@pytest.mark.parametrize(
	"description,price,expected_points",
	[
		("foo","6.00",2),
		("bar","10.32",3),
		("ep","10.32",0),
		("this is a short description","0.00",0),
	]
)
def test_calculate_description_points(description, price, expected_points):
	datum = {"shortDescription": description, "price": price}
	formatted_price = float(price)
	points = Item(datum).calculate_description_points()
	assert points == expected_points