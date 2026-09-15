import os

os.environ["TESTING"] = "1"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_conversation(name="Rahul"):
    return client.post(
        "/conversations",
        json={
            "customer_name": name,
            "message": "Do you have the black hoodie in medium?",
            "intent": "purchase_intent",
        },
    )


def create_order(conversation_id):
    return client.post(
        "/orders",
        json={
            "conversation_id": conversation_id,
            "product": "Black Hoodie - Medium",
            "amount": 2499,
        },
    )


def test_root_endpoint():
    reset_database()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "TraceCart"


def test_create_conversation():
    reset_database()
    response = create_conversation()
    assert response.status_code == 201
    assert response.json()["intent"] == "purchase_intent"


def test_create_order():
    reset_database()
    conversation = create_conversation().json()
    response = create_order(conversation["id"])
    assert response.status_code == 201
    assert response.json()["conversation_id"] == conversation["id"]


def test_create_attribution():
    reset_database()
    conversation = create_conversation().json()
    order = create_order(conversation["id"]).json()

    response = client.post(
        "/attributions",
        json={
            "conversation_id": conversation["id"],
            "order_id": order["id"],
            "reason": "Customer purchase originated from the conversation",
        },
    )
    assert response.status_code == 201
    assert response.json()["order_id"] == order["id"]


def test_invalid_conversation_returns_404():
    reset_database()
    response = create_order(999)
    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"


def test_invalid_order_returns_404():
    reset_database()
    conversation = create_conversation().json()
    response = client.post(
        "/attributions",
        json={
            "conversation_id": conversation["id"],
            "order_id": 999,
            "reason": "Invalid order test",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_wrong_relationship_returns_400():
    reset_database()
    conversation_1 = create_conversation("Rahul").json()
    conversation_2 = create_conversation("Anita").json()
    order_2 = create_order(conversation_2["id"]).json()

    response = client.post(
        "/attributions",
        json={
            "conversation_id": conversation_1["id"],
            "order_id": order_2["id"],
            "reason": "Wrong relationship test",
        },
    )
    assert response.status_code == 400


def test_duplicate_attribution_returns_409():
    reset_database()
    conversation = create_conversation().json()
    order = create_order(conversation["id"]).json()
    payload = {
        "conversation_id": conversation["id"],
        "order_id": order["id"],
        "reason": "Customer purchase originated from the conversation",
    }

    first_response = client.post("/attributions", json=payload)
    second_response = client.post("/attributions", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
