from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TraceCart — Conversation Attribution API",
    description="A small backend prototype demonstrating conversation-level e-commerce attribution.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "name": "TraceCart",
        "message": "Conversation Attribution API is running",
    }


@app.post(
    "/conversations",
    response_model=schemas.ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    conversation: schemas.ConversationCreate,
    db: Session = Depends(get_db),
):
    db_conversation = models.Conversation(**conversation.model_dump())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


@app.get("/conversations", response_model=list[schemas.ConversationResponse])
def get_conversations(db: Session = Depends(get_db)):
    return db.query(models.Conversation).order_by(models.Conversation.id).all()


@app.post(
    "/orders",
    response_model=schemas.OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    conversation = db.get(models.Conversation, order.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders", response_model=list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).order_by(models.Order.id).all()


@app.post(
    "/attributions",
    response_model=schemas.AttributionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_attribution(
    attribution: schemas.AttributionCreate,
    db: Session = Depends(get_db),
):
    conversation = db.get(models.Conversation, attribution.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    order = db.get(models.Order, attribution.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.conversation_id != attribution.conversation_id:
        raise HTTPException(
            status_code=400,
            detail="Order does not belong to the specified conversation",
        )

    existing_attribution = (
        db.query(models.Attribution)
        .filter(models.Attribution.order_id == attribution.order_id)
        .first()
    )
    if existing_attribution:
        raise HTTPException(
            status_code=409,
            detail="This order already has an attribution",
        )

    db_attribution = models.Attribution(**attribution.model_dump())
    db.add(db_attribution)
    db.commit()
    db.refresh(db_attribution)
    return db_attribution


@app.get("/attributions", response_model=list[schemas.AttributionResponse])
def get_attributions(db: Session = Depends(get_db)):
    return db.query(models.Attribution).order_by(models.Attribution.id).all()
