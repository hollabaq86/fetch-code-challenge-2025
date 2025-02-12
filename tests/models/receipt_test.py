import pytest
from src.models.receipt import Receipt
from src.models.item import Item


@pytest.mark.parametrize(
    "retailer,purchase_date,purchase_time,items,total,expected_count",
    [
        (
            "Target",
            "2022-01-02",
            "13:13",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            6,
        ),
        (
            "Walgreens",
            "2022-01-02",
            "08:13",
            [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"},
            ],
            "2.65",
            15,
        ),
    ],
)
def test_receipt(retailer, purchase_date, purchase_time, items, total, expected_count):
    datum = {
        "retailer": retailer,
        "purchaseDate": purchase_date,
        "purchaseTime": purchase_time,
        "items": items,
        "total": total,
    }
    receipt = Receipt(datum)
    assert receipt is not None
    assert receipt.id is not None
    assert receipt.retailer == retailer
    assert receipt.purchase_date == purchase_date
    assert receipt.purchase_time == purchase_time
    assert receipt.total == float(total)
    assert receipt.points == expected_count
    item_zero = receipt.items[0]
    assert item_zero is not None
    assert isinstance(item_zero, Item)
    assert item_zero.short_description == items[0]["shortDescription"]
    assert item_zero.price == float(items[0]["price"])
    assert item_zero.description_points == 0
    if len(items) > 1:
        item_one = receipt.items[1]
        assert item_one is not None
        assert isinstance(item_one, Item)
        assert item_one.short_description == items[1]["shortDescription"]
        assert item_one.price == float(items[1]["price"])
        assert item_one.description_points == 1


@pytest.mark.parametrize(
    "retailer,purchase_date,purchase_time,items,total,expected_points",
    [
        (
            "Target",
            "2022-01-02",
            "13:13",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            6,
        ),
        (
            "Target",
            "2022-01-01",
            "13:01",
            [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
            ],
            "35.35",
            28,
        ),
        (
            "M&M Corner Market",
            "2022-03-20",
            "14:33",
            [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
            ],
            "9.00",
            109,
        ),
    ],
)
def test_assign_points(
    retailer, purchase_date, purchase_time, items, total, expected_points
):
    datum = {
        "retailer": retailer,
        "purchaseDate": purchase_date,
        "purchaseTime": purchase_time,
        "items": items,
        "total": total,
    }

    points = Receipt(datum).assign_points()
    assert points == expected_points


@pytest.mark.parametrize(
    "retailer,expected_count",
    [
        ("Target", 6),
        ("Walgreens", 9),
        ("Super Mart 123", 12),
        ("!Buy Things%", 9),
    ],
)
def test_assign_points_counts_retailer_alphanumeric_characters(
    retailer, expected_count
):
    datum = {
        "retailer": retailer,
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "items": [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
        "total": "1.31",
    }

    points = Receipt(datum).assign_points()
    assert points == expected_count


@pytest.mark.parametrize(
    "total,expected_count",
    [
        ("1.23", 6),
        ("2.25", 31),
        ("2.00", 81),
        ("3", 81),
    ],
)
def test_assign_points_counts_checks_total_whole_number(total, expected_count):
    datum = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "items": [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
        "total": total,
    }

    points = Receipt(datum).assign_points()
    assert points == expected_count


@pytest.mark.parametrize(
    "items,expected_count",
    [
        ([{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}], 6),
        (
            [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            ],
            11,
        ),
        (
            [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            ],
            11,
        ),
        (
            [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            ],
            16,
        ),
    ],
)
def test_assign_points_checks_number_of_items(items, expected_count):
    datum = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "items": items,
        "total": "1.23",
    }

    points = Receipt(datum).assign_points()
    assert points == expected_count


@pytest.mark.parametrize(
    "items,expected_count",
    [
        ([{"shortDescription": "Dasani", "price": "1.25"}], 7),
        (
            [
                {"shortDescription": "Dasani", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.25"},
            ],
            13,
        ),
        (
            [
                {"shortDescription": "Dasani", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.25"},
            ],
            14,
        ),
        (
            [
                {"shortDescription": "Dasani", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.25"},
            ],
            20,
        ),
    ],
)
def test_assign_points_item_descriptions(items, expected_count):
    datum = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "items": items,
        "total": "1.23",
    }

    points = Receipt(datum).assign_points()
    assert points == expected_count


@pytest.mark.parametrize(
    "retailer,purchase_date,purchase_time,items,total,expected_points",
    [
        (
            "Target",
            "2022-01-02",
            "13:13",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            6,
        ),
        (
            "Target",
            "2022-01-01",
            "13:13",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            12,
        ),
    ],
)
def test_assign_points_checks_purchase_date(
    retailer, purchase_date, purchase_time, items, total, expected_points
):
    datum = {
        "retailer": retailer,
        "purchaseDate": purchase_date,
        "purchaseTime": purchase_time,
        "items": items,
        "total": total,
    }

    points = Receipt(datum).assign_points()
    assert points == expected_points


@pytest.mark.parametrize(
    "retailer,purchase_date,purchase_time,items,total,expected_points",
    [
        (
            "Target",
            "2022-01-02",
            "13:13",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            6,
        ),
        (
            "Target",
            "2022-01-01",
            "14:13",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            22,
        ),
        (
            "Target",
            "2022-01-01",
            "16:13",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            12,
        ),
        (
            "Target",
            "2022-01-01",
            "16:00",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            22,
        ),
        (
            "Target",
            "2022-01-01",
            "14:00",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            22,
        ),
        (
            "Target",
            "2022-01-01",
            "15:13",
            [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            "1.31",
            22,
        ),
    ],
)
def test_assign_points_checks_purchase_time(
    retailer, purchase_date, purchase_time, items, total, expected_points
):
    datum = {
        "retailer": retailer,
        "purchaseDate": purchase_date,
        "purchaseTime": purchase_time,
        "items": items,
        "total": total,
    }

    points = Receipt(datum).assign_points()
    assert points == expected_points
