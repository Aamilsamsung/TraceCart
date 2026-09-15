from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1)
    intent: str = Field(min_length=1, max_length=100)


class ConversationResponse(ConversationCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    conversation_id: int = Field(gt=0)
    product: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)


class OrderResponse(OrderCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AttributionCreate(BaseModel):
    conversation_id: int = Field(gt=0)
    order_id: int = Field(gt=0)
    reason: str = Field(min_length=1)


class AttributionResponse(AttributionCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
