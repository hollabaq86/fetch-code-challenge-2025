# fetch-code-challenge-2025
Fetch code challenge solution! This solution is built using python, uv, and flask.


## running the app
Use docker to spin up the app:

```
docker build -t app .
docker run --rm -it -p 8080:5000 app
```

Once running, curl requests can be made to local port 8080 from another terminal window:

```
curl \
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
-D- \
  http://127.0.0.1:8080/receipts/process
```

Alternatively, run the test script to fire off a bunch of test curl commands:
```
bash test_curl.sh
```

## tests
Tests can also be run from docker:

```
docker build -t app .
docker run app /bin/bash -l -c "uv run pytest"
```