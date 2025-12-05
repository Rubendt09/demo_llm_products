from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """
    Modelo de Producto para la base de datos
    Representa los productos de tecnología de la tienda
    """
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)  # S001, M005, T010
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, stock={self.stock})>"