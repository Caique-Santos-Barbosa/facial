"""
Script para inicializar banco de dados e criar usuário admin
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash

def init_db():
    """Inicializa banco de dados"""
    # Cria tabelas
    Base.metadata.create_all(bind=engine)
    
    # Cria sessão
    db = SessionLocal()
    
    try:
        # Verifica se já existe admin
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            # Cria usuário admin padrão
            admin = User(
                username="admin",
                email="admin@hdtenergy.com",
                hashed_password=get_password_hash("admin123"),  # MUDAR EM PRODUÇÃO!
                full_name="Administrador",
                is_superuser=True,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✅ Usuário admin criado com sucesso!")
            print("   Username: admin")
            print("   Password: admin123")
            print("   ⚠️  IMPORTANTE: Altere a senha em produção!")
        else:
            print("ℹ️  Usuário admin já existe")
    
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando banco de dados...")
    init_db()
    print("✅ Banco de dados inicializado!")
