import json
import pytest
from httpx import AsyncClient
import anyio
from ..app.main import app
@pytest.mark.anyio
async def test_create_item():
    # Create a test client
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Define the item data to be sent in the request body
        item_data = {
            "item_code": 123,
            "item_name": "Test Item",
            "tag": ["tag1", "tag2"],
            "description": "Test description",
            "price": 9.99,
            "quantity": 10
        }

        # Send a POST request to the create_item endpoint
        response = await client.post("/item/", json=item_data)

        # Check the response status code
        assert response.status_code == 200

        # Parse the response JSON
        created_item = response.json()

        # Check the item details in the response
        assert created_item["item_code"] == item_data["item_code"]
        assert created_item["item_name"] == item_data["item_name"]
        assert created_item["tag"] == item_data["tag"]
        assert created_item["description"] == item_data["description"]
        assert created_item["price"] == item_data["price"]
        assert created_item["quantity"] == item_data["quantity"]
        
        
