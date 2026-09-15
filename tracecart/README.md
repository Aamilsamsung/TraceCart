# TraceCart — Conversation Attribution API

TraceCart is a small backend prototype exploring **conversation-level e-commerce attribution**.

It demonstrates a simple relationship:

```text
Customer Conversation
        ↓
Conversation Record
        ↓
      Order
        ↓
Attribution Record
```

## Problem

Traditional marketing attribution can make it difficult to determine exactly which customer interaction resulted in a purchase. TraceCart explores a simple approach where a customer conversation and the resulting order are explicitly connected.

## Features

- Conversation management
- Customer intent storage
- Order management
- Conversation/order relationships
- Attribution records
- Relationship validation
- Duplicate-attribution protection
- REST API
- Swagger and ReDoc documentation
- Automated tests

## Technology

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Uvicorn

## Project structure

```text
tracecart/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate it on Windows

Command Prompt:

```bat
venv\Scripts\activate
```

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Example workflow

### 1. Create a conversation

`POST /conversations`

```json
{
  "customer_name": "Rahul",
  "message": "Do you have the black hoodie in medium?",
  "intent": "purchase_intent"
}
```

### 2. Create an order

`POST /orders`

```json
{
  "conversation_id": 1,
  "product": "Black Hoodie - Medium",
  "amount": 2499
}
```

### 3. Create an attribution

`POST /attributions`

```json
{
  "conversation_id": 1,
  "order_id": 1,
  "reason": "Customer purchase originated from the conversation"
}
```

### 4. Retrieve attribution records

`GET /attributions`

## Validation behavior

TraceCart checks that:

- an order's conversation exists;
- an attribution's conversation exists;
- an attribution's order exists;
- an order belongs to the conversation used in the attribution;
- an order cannot receive more than one attribution.

Expected errors include `404 Not Found`, `400 Bad Request`, and `409 Conflict`.

## Run tests

```bash
pytest -v
```

## Portfolio description

> Built a FastAPI prototype exploring conversation-level e-commerce attribution, connecting customer conversations to orders through validated attribution records.

## Scope

This is a learning and portfolio project, not a production-ready attribution platform. Possible future improvements include PostgreSQL, Redis, background workers, authentication, monitoring, cloud deployment, Shopify/Meta integrations, vector search, and LLM-based intent classification.
