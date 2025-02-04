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
	assert item.price == price
