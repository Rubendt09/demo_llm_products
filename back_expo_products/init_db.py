"""
Script de inicialización de base de datos
Crea las tablas de la base de datos
"""
from app.database import engine, Base


def init_db():
    """Inicializa la base de datos creando las tablas"""
    
    # Crear todas las tablas
    print("🔨 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")
    print("\n💡 Usa el archivo seed_products.sql para cargar productos de demo")


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Inicializando Base de Datos para Demo")
    print("=" * 50)
    init_db()
    print("\n" + "=" * 50)
    print("✨ Inicialización completada")
    print("=" * 50)