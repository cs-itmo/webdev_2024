#!/bin/bash
curl -X POST "http://127.0.0.1:8000/items" \
-H "Content-Type: application/json" \
-d '{
  "name": "Sample Item",
  "description": "This is a sample item",
  "price": 19.99,
  "in_stock": true
}'

curl -X GET "http://127.0.0.1:8000/items/3081cbb1-e02c-479e-91d4-c76216895602"

curl -X PUT "http://127.0.0.1:8000/items/3081cbb1-e02c-479e-91d4-c76216895602" \
-H "Content-Type: application/json" \
-d '{
  "name": "Updated Item",
  "description": "This is an updated item",
  "price": 29.99,
  "in_stock": false
}'

curl -X DELETE "http://127.0.0.1:8000/items/3081cbb1-e02c-479e-91d4-c76216895602"

curl -X GET "http://127.0.0.1:8000/items"

curl -X GET "http://127.0.0.1:8000/items?name=Sample"
