import pytest
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine

# Create a test database session
@pytest.fixture(scope="module")
def db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        models.Base.metadata.drop_all(bind=engine)

def test_create_user(db: Session):
    user_in = schemas.UserCreate(email="test@example.com", password="testpassword")
    user = crud.create_user(db=db, user=user_in)
    assert user.email == "test@example.com"
    assert user.hashed_password == "testpasswordnotreallyhashed"

def test_get_user(db: Session):
    user = crud.get_user(db=db, user_id=1)
    assert user.email == "test@example.com"

def test_get_user_by_email(db: Session):
    user = crud.get_user_by_email(db=db, email="test@example.com")
    assert user.email == "test@example.com"

def test_get_users(db: Session):
    users = crud.get_users(db=db, skip=0, limit=10)
    assert len(users) == 1
    assert users[0].email == "test@example.com"

def test_create_user_item(db: Session):
    item_in = schemas.ItemCreate(title="Test Item", description="This is a test item")
    item = crud.create_user_item(db=db, item=item_in, user_id=1)
    assert item.title == "Test Item"
    assert item.description == "This is a test item"
    assert item.owner_id == 1

def test_get_items(db: Session):
    items = crud.get_items(db=db, skip=0, limit=10)
    assert len(items) == 1
    assert items[0].title == "Test Item"
