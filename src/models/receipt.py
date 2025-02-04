from typing import Dict
from models.item import Item

class Receipt():
	def __init__(self, datum: Dict):
		self.retailer = datum["retailer"]
		self.purchase_date = datum["purchaseDate"]
		self.purchase_time = datum["purchaseTime"]
		self.items = [Item(item) for item in datum["items"]]
		self.total = datum["total"]

