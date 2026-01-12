"""
Script para inicializar o banco de dados e criar usuário admin
Execute: python -m scripts.init_db
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash

def init_db():
    """Cria as tabelas e um usuário admin padrão"""
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Verifica se já existe um admin
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            # Cria usuário admin padrão
            admin = User(
                username="admin",
                email="admin@hdtenergy.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrador",
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("✅ Usuário admin criado com sucesso!")
            print("   Usuário: admin")
            print("   Senha: admin123")
            print("   ⚠️  ALTERE A SENHA APÓS O PRIMEIRO LOGIN!")
        else:
            print("ℹ️  Usuário admin já existe")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

