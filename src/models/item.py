from typing import Dict


class Item:
    def __init__(self, datum: Dict):
        self.short_description = datum["shortDescription"]
        self.price = float(datum["price"])
        self.description_points = self.calculate_description_points()

    def calculate_description_points(self):
        length_trimmed = len(self.short_description.strip())
        if length_trimmed > 2 and length_trimmed % 3 == 0 and self.price > 0:
            return int(self.price * 0.2) + 1
        return 0
