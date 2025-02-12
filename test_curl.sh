## RECEIPT ONE ##

echo -e "***First POST request:"
RECEIPT_ID=$(curl \
  -s \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "13:13",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
}' \
  http://127.0.0.1:8080/receipts/process \
  | awk -F'"' '$2=="id"{printf("%s", $4)}'
  )

echo -e 'created receipt:\n "id": "'"$RECEIPT_ID"'"'
echo -e "First GET request, getting points"

POINTS=$(curl \
  -s \
  --header "Content-Type: application/json" \
  --request GET \
  http://127.0.0.1:8080/receipts/$RECEIPT_ID/points \
  | awk -F'"' '$2=="points"{printf("%s", $0)}')
echo "$POINTS"

## RECEIPT TWO ##

echo -e "\n***Second POST request:"
RECEIPT_ID=$(curl \
  -s \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{
    "retailer": "Walgreens",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "08:13",
    "total": "2.65",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
        {"shortDescription": "Dasani", "price": "1.40"}
    ]
}' \
  http://127.0.0.1:8080/receipts/process \
  | awk -F'"' '$2=="id"{printf("%s", $4)}'
  )

echo -e 'created receipt:\n "id": "'"$RECEIPT_ID"'"'
echo -e "Second GET request, getting points"

POINTS=$(curl \
  -s \
  --header "Content-Type: application/json" \
  --request GET \
  http://127.0.0.1:8080/receipts/$RECEIPT_ID/points \
  | awk -F'"' '$2=="points"{printf("%s", $0)}')
echo "$POINTS"

## RECEIPT THREE ##

echo -e "\n***Third POST request:"
RECEIPT_ID=$(curl \
  -s \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}' \
  http://127.0.0.1:8080/receipts/process \
  | awk -F'"' '$2=="id"{printf("%s", $4)}'
  )

echo -e 'created receipt:\n "id": "'"$RECEIPT_ID"'"'
echo -e "Third GET request:"

POINTS=$(curl \
  -s \
  --header "Content-Type: application/json" \
  --request GET \
  http://127.0.0.1:8080/receipts/$RECEIPT_ID/points \
  | awk -F'"' '$2=="points"{printf("%s", $0)}')
echo "$POINTS"

## RECEIPT FOUR ##

echo -e "\n***Fourth POST request:"
RECEIPT_ID=$(curl \
  -s \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}' \
  http://127.0.0.1:8080/receipts/process \
  | awk -F'"' '$2=="id"{printf("%s", $4)}'
  )


echo -e 'created receipt:\n "id": "'"$RECEIPT_ID"'"'
echo -e "Fourth GET request:"

POINTS=$(curl \
  -s \
  --header "Content-Type: application/json" \
  --request GET \
  http://127.0.0.1:8080/receipts/$RECEIPT_ID/points \
  | awk -F'"' '$2=="points"{printf("%s", $0)}')
echo "$POINTS"

## SAD PATH EDGE CASES

echo -e "\n***Sad path POST requests:"
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{
  "retailer": "M&M Corner Market",
  "notValid": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}' \
  http://127.0.0.1:8080/receipts/process \
  -D-

  echo -e "\n***Sad path GET requests:"
curl \
  --header "Content-Type: application/json" \
  --request GET \
  http://127.0.0.1:8080/receipts/not-real/points \
  -D-