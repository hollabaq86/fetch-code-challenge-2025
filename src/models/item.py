from typing import Dict

class Item():
	def __init__(self, datum:Dict):
		self.short_description = datum["shortDescription"]
		self.price = datum["price"]