from typing import Dict, List
from models.item import Item
from uuid_utils import uuid7


class Receipt:
    def __init__(self, datum: Dict):
        self.source_datum = datum
        self.retailer = datum["retailer"]
        self.purchase_date = datum["purchaseDate"]
        self.purchase_time = datum["purchaseTime"]
        self.items = [Item(item) for item in datum["items"]]
        self.total = float(datum["total"])
        self.id = str(uuid7())
        self.points = self.assign_points()

    def assign_points(self):
        points = 0
        number_of_items = len(self.items)
        if self.retailer is not None:
            points += _count_alphanumeric_characters(self.retailer)
        if self.total is not None:
            points += _calculate_total_price_points(
                total=self.total, source_total=self.source_datum["total"]
            )
        if number_of_items > 1:
            points += _calculate_number_of_items_points(number_of_items)
        if number_of_items > 0:
            points += _calculate_item_description_points(self.items)
        if self.purchase_date is not None:
            points += _calculate_purchase_date_points(self.purchase_date)
        if self.purchase_time is not None:
            points += _calculate_purchase_time_points(self.purchase_time)
        return points


def _count_alphanumeric_characters(input_string: str):
    count = 0
    for x in input_string:
        if x.isalnum():
            count += 1

    return count


def _calculate_total_price_points(total: float, source_total: str):
    if ".00" in source_total:
        return 75  # 50 for whole number plus divisible by .25
    for compare_string in [".25", ".50", ".75"]:
        if compare_string in source_total:
            return 25  # just divisible by .25
    # edge case if price doesn't include a decimal point for .00
    try:
        if int(source_total) == total:
            return 75
    except ValueError:  # noop, total was a float string, not divisible
        return 0


def _calculate_number_of_items_points(number_of_items: int):
    if number_of_items % 2 == 0:
        return int(number_of_items / 2) * 5
    else:
        return int((number_of_items - 1) / 2) * 5


def _calculate_item_description_points(items: List[Item]):
    points = 0
    for item in items:
        points += item.description_points

    return points


def _calculate_purchase_date_points(purchase_date: str):
    date = purchase_date[-2:]
    if int(date) % 2 == 1:
        return 6
    return 0


def _calculate_purchase_time_points(purchase_time: str):
    hour = int(purchase_time[:2])
    minutes = int(purchase_time[-2:])

    if hour > 13 < 17:
        if hour == 16 and minutes > 0:
            return 0
        return 10
    return 0
