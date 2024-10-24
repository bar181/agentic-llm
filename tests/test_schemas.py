import pytest
from pydantic import ValidationError
from app.schemas import ItemCreate, UserCreate

def test_item_create_schema():
    item = ItemCreate(title="Test Item", description="This is a test item")
    assert item.title == "Test Item"
    assert item.description == "This is a test item"

def test_item_create_schema_validation_error():
    with pytest.raises(ValidationError):
        ItemCreate(title="Test Item")

def test_user_create_schema():
    user = UserCreate(email="test@example.com", password="testpassword")
    assert user.email == "test@example.com"
    assert user.password == "testpassword"

def test_user_create_schema_validation_error():
    with pytest.raises(ValidationError):
        UserCreate(email="test@example.com")
