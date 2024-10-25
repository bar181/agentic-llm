import pytest
from pydantic import ValidationError
from app.models import Item, User

def test_create_item():
    item = Item(title="Test Item", description="This is a test item", owner_id=1)
    assert item.title == "Test Item"
    assert item.description == "This is a test item"
    assert item.owner_id == 1

def test_create_user():
    user = User(email="test@example.com", password="testpassword")
    assert user.email == "test@example.com"
    assert user.password == "testpassword"

def test_item_validation_error():
    with pytest.raises(ValidationError):
        Item(title="Test Item", description="This is a test item")

def test_user_validation_error():
    with pytest.raises(ValidationError):
        User(email="test@example.com")
