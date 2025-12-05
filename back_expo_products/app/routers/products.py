from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse, StockResponse, PricingResponse

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)


@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """
    Obtiene todos los productos disponibles
    """
    products = db.query(Product).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: str, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por su ID
    
    Args:
        product_id: ID del producto (ej: S001, M005, T010)
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    return product


@router.get("/{product_id}/stock", response_model=StockResponse)
def get_product_stock(product_id: str, db: Session = Depends(get_db)):
    """
    Verifica la disponibilidad de inventario para un producto específico
    
    Args:
        product_id: ID del producto a verificar (ej: S001, M005, T010)
    
    Returns:
        StockResponse con información de disponibilidad en tiempo real
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    return StockResponse(
        product_id=product.id,
        product_name=product.name,
        stock=product.stock,
        status="Disponible" if product.stock > 0 else "Agotado"
    )


@router.get("/{product_id}/pricing", response_model=PricingResponse)
def get_product_pricing(product_id: str, db: Session = Depends(get_db)):
    """
    Obtiene el precio actual de un producto
    
    Args:
        product_id: ID del producto a consultar (ej: S001, M005, T010)
    
    Returns:
        PricingResponse con información de precio actualizada
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    return PricingResponse(
        product_id=product.id,
        price=product.price,
        currency="USD"
    )


@router.get("/search/query", response_model=List[ProductResponse])
def search_products(
    q: str = Query(..., description="Término de búsqueda"),
    limit: int = Query(5, ge=1, le=20, description="Máximo de resultados (1-20)"),
    db: Session = Depends(get_db)
):
    """
    Busca productos por nombre o descripción
    
    Args:
        q: Término de búsqueda (ej: 'gaming', 'laptop', 'monitor')
        limit: Número máximo de resultados (default: 5, max: 20)
    
    Returns:
        Lista limitada de productos que coinciden con la búsqueda
    """
    search_term = f"%{q}%"
    
    products = db.query(Product).filter(
        or_(
            Product.name.ilike(search_term),
            Product.description.ilike(search_term)
        )
    ).limit(limit).all()
    
    return products


@router.get("/summary/catalog")
def get_catalog_summary(db: Session = Depends(get_db)):
    """
    Obtiene un resumen simplificado del catálogo
    
    Retorna solo: ID, nombre y precio (sin descripciones)
    
    Returns:
        Lista simplificada de productos
    """
    products = db.query(
        Product.id,
        Product.name,
        Product.price
    ).all()
    
    return {
        "total": len(products),
        "catalog": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price
            }
            for p in products
        ]
    }