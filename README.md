# TraceCart — Conversation Attribution API

A small FastAPI backend prototype exploring **conversation-level e-commerce attribution**.

> **Portfolio / learning project:** TraceCart is not affiliated with SentLogic and does not use SentLogic code, branding, or proprietary implementation.

## What is TraceCart?

TraceCart demonstrates a simple relationship:

```text
Customer Conversation
        ↓
Conversation Record
        ↓
      Order
        ↓
Attribution Record
```

The goal is to answer a simple question:

**Which customer conversation resulted in this order?**

## Features

- Create and list customer conversations
- Store customer intent
- Create and list orders
- Connect orders to conversations
- Create and list attribution records
- Validate conversation/order relationships
- Return useful HTTP errors
- Prevent duplicate attribution for an order
- Automatic Swagger and ReDoc documentation
- Automated Pytest coverage for the core API behavior

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

Open Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

ReDoc is available at:

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

- an order's conversation exists (`404` if it does not);
- an attribution's conversation exists (`404` if it does not);
- an attribution's order exists (`404` if it does not);
- the order belongs to the conversation used in the attribution (`400` if it does not);
- an order cannot receive more than one attribution (`409` if it already has one).

## Run tests

```bash
pytest -v
```

## Portfolio description

> Built a FastAPI prototype exploring conversation-level e-commerce attribution, connecting customer conversations to orders through validated attribution records.

## Scope and future improvements

This is a learning and portfolio project, not a production-ready attribution platform. Possible future improvements include PostgreSQL, Redis, background workers, authentication, monitoring, cloud deployment, Shopify/Meta integrations, vector search, and LLM-based intent classification.
