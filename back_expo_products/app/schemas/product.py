from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    """Schema base para Producto"""
    id: str
    name: str
    description: str
    price: float
    stock: int


class ProductResponse(ProductBase):
    """Schema para respuesta de Producto con timestamps"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StockResponse(BaseModel):
    """Schema para respuesta de consulta de stock"""
    product_id: str
    product_name: str
    stock: int
    status: str  # "Disponible" o "Agotado"

    class Config:
        from_attributes = True


class PricingResponse(BaseModel):
    """Schema para respuesta de consulta de precio"""
    product_id: str
    price: float
    currency: str = "USD"

    class Config:
        from_attributes = True